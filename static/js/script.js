window.addEventListener("load", () => {
var status = localStorage.getItem("active");

  if (status == 0) {
    lightmode(status);
  } else {
    darkmode(status);
  }
  document.getElementById("loadingSpinner").style.display = "none";
  setTimeout(() => {
    document.getElementById("loadingSpinner").style.display = "none";
  }, 200);
});

var status = localStorage.getItem("active");

if (status == 0) {
  lightmode(status);
} else {
  darkmode(status);
}
function lightmode(active) {
  $("body").addClass("dark-mode");
  localStorage.setItem("active", active);
  $(".darkmode").css("display", "block");
  $(".lightmode").css("display", "none");
}
function darkmode(active) {
  $("body").removeClass("dark-mode");
  localStorage.setItem("active", active);
  $(".darkmode").css("display", "none");
  $(".lightmode").css("display", "block");
}
$(document).ready(function () {
  $("#darkModeSwitch").click(function () {
    active = 0;
    active = localStorage.getItem("active");

    if (active == 0) {
      active = 1;
      darkmode(active);
    } else {
      active = 0;
      lightmode(active);
    }
  });
});

// for sidebar in admin panel

$(".leftarrow").click(function () {
  var sidebar = $(".sidebar");
  if (sidebar.css("width") == "250px") {
    $(".sidebar").css({
      width: "60px",
      transition: "width 0.5s ease-out", // Adjust duration and timing function as needed
    });
    $(".sidebartitle").hide(100);
    $(".til").css("text-align", "center");
    $(this).css("rotate", "180deg");
  } else {
    sidebar.css("width", "250px");
    $(".sidebartitle").show();
    $(".til").css("text-align", "left");
    $(this).css("rotate", "0deg");
  }
});

// end

$("#slug").on("input", function () {
  var text = $(this).val().replace(/\s+/g, "-");
  $(this).val(text);
});

// for password hide show icon
$("#eye").click(function () {
  var pass = $(".password");
  if (pass.attr("type") === "password") {
    pass.attr("type", "text");
    $(".fa-eye").css("font-weight", 900);
  } else {
    pass.attr("type", "password");
    $(".fa-eye").css("font-weight", 400);
  }
});

// for close model
$("#closemodelbtn").click(function () {
  $("#exampleModal").css("display", "none");
});
// for hide and show usericon popover

$("#usericon").click(function () {
  var popover = $("#profilepop");
  if (popover.css("display") == "none") {
    $("#profilepop").removeClass("pop");
    $("#profilepop").addClass("popov");
  } else {
    $("#profilepop").addClass("pop");
    $("#profilepop").removeClass("popov");
  }
});

// for search bar

$("#searchInput").on("keyup", function () {
  var searchText = $(this).val().toLowerCase();
  var currentpage = $("#currentpage").val();
  console.log(currentpage);

  $.ajax({
    url: "/search/", // URL to your search endpoint in Django
    type: "GET", // You might need to change the type based on your implementation
    data: { query: searchText, currentpage:currentpage }, // Send the search query as data
    dataType: "json",
    success: function (data) {
      $(".article").each(function (index, element) {
        var title = $(element).find(".card-title").text().toLowerCase();
        var description = $(element).find(".card-text").text().toLowerCase();
        if (
          title.indexOf(searchText) === -1 &&
          description.indexOf(searchText) === -1
        ) {
          $(element).hide();
        } else {
          $(element).show();
        }
      });
    },
    error: function (error) {
      console.log("Error occurred: ", error);
    },
  });
});
// for saving createpost.html text in localStorage

function saveContentToLocalStorage() {
  var content = tinymce.activeEditor.getContent();
  localStorage.setItem("savedContent", content);
}
function loadContentFromLocalStorage() {
  var savedContent = localStorage.getItem("savedContent");
  if (savedContent) {
    tinymce.activeEditor.setContent(savedContent);
  }
}

// for signin and signup code and ajax and validations
message = "";

function checkingvalidation() {
  active = true;
  var email = $(".email").val();
  var password = $(".password").val();
  var firstname = $(".firstname").val();
  var lastname = $(".lastname").val();
  if (password.length <= 5) {
    active = false;
    message = "Password is too short";
  }
  if (email == "" || password == "" || firstname == "" || lastname == "") {
    active = false;
    message = "Please fill the form";
  }

  $(".email").on("input", function () {
    var email = $(".email").val();
    var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var maxLength = 50;
    if (email.length < maxLength) {
      if (!emailPattern.test(email)) {
        if (email === "") {
          $(".email").css("border-color", "#dee2e6");
          // active=localStorage.setItem('active',false);
          active = false;
        } else {
          $(".email").css("border-color", "red");
          // active=localStorage.setItem('active',false);
          active = false;
        }
      } else {
        $(".email").css("border-color", "#dee2e6");
      }
    } else {
      text = email.slice(0, maxLength);
      $(this).val(text);
    }
    return active;
  });

  $(".password").on("input", function () {
    var password = $(this).val();
    var sanitizedPassword = password.replace(/[^a-zA-Z0-9@#]/g, ""); // Remove characters not allowed
    var maxLength = 15;
    if (sanitizedPassword.length > maxLength) {
      sanitizedPassword = sanitizedPassword.slice(0, maxLength);
    }
    $(this).val(sanitizedPassword); // Update input value with sanitized text
  });
  $(".firstname, .lastname").on("input", function () {
    var name = $(this).val();
    var sanitizedPassword = name.replace(/[^a-zA-Z]/g, "");
    var maxLength = 15;
    if (sanitizedPassword.length > maxLength) {
      sanitizedPassword = name.slice(0, maxLength); // Truncate the input if it exceeds the maximum length
    }
    $(this).val(sanitizedPassword); // Update input value with truncated text
  });
  return active;
}
$(document).ready(function () {
  function formcheck() {
    active = true;
    if ($("#email").val() === "" || $("#password").val() === "") {
      active = false;
    }
    return active;
  }
  $("#signinButton").click(function (e) {
    e.preventDefault(); // Prevent the default form submission
    var formData = {
      email: $("#email").val(),
      password: $("#password").val(),
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
    };
    check = formcheck();
    if (check == true) {
      $.ajax({
        url: "/signin/",
        type: "POST",
        data: formData,
        dataType: "json",
        beforeSend: function (xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", formData.csrfmiddlewaretoken);
        },
        success: function (data) {
          if (data.message === true) {
            window.location.href = "/";
          } else {
            $(".custom-alert").show();
            $("#alerttext").text("Email & Password does not match.");
            $("#alerttext").css("color", "black");
            $(".custom-alert").css("background-color", "#ffc436");
            var borderElement = $(".custom-alert-border");
            borderElement.css("width", "100%");
            borderElement.animate({ width: 0 }, function () {
              setTimeout(function () {
                $(".custom-alert").hide();
              }, 1400);
            });
          }
        },
        error: function (error) {},
      });
    } else {
      $(".custom-alert").show();
      $("#alerttext").text("Please fill the form.");
      $("#alerttext").css("color", "white");
      $(".custom-alert").css("background-color", "#860A35");
      var borderElement = $(".custom-alert-border");
      borderElement.css("width", "100%");
      borderElement.animate({ width: 0 }, function () {
        setTimeout(function () {
          $(".custom-alert").hide();
        }, 1400);
      });
    }
  });

  //  for forgotpassword

  $("#forgotpassword").click(function () {
    $(this).hide();
    $("#signinButton").attr("type", "button");
    $(".back").show();
    $(".forgotpasswordhide").hide();
    $(".forgotpasswordchangetext").text("Enter Recovery Email");
    $("#signinButton").hide();
    $(".forgotbutton").show();

    $(".forgotbutton").click(function (e) {
      $("#signinButton").attr("type", "button");
      e.preventDefault();
      $(".forgotbutton").text("Please Wait...");
      var email = $("#email").val();
      var csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); // Fetch the CSRF token from the page

      var data = {
        email: email,
        condition: 1,
        csrfmiddlewaretoken: csrfToken, // Set the CSRF token in your data object
      };

      $.ajax({
        url: "/forgotpassword/",
        type: "POST",
        data: data,
        dataType: "json",
        beforeSend: function (xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", csrfToken); // Set CSRF token in request header
        },
        success: function (data) {
          $(".forgotbutton").text("Send Code");
          if (data.message == true) {
            $(".custom-alert").show();
            $("#alerttext").text("User with this email does not exist");
            $("#alerttext").css("color", "black");
            $(".custom-alert").css("background-color", "#FFC436");
            var borderElement = $(".custom-alert-border");
            borderElement.css("width", "100%");
            borderElement.animate(
              {
                width: 0,
              },
              function () {
                setTimeout(function () {
                  $(".custom-alert").hide();
                }, 1400);
              }
            );
          } else {
            $("#exampleModal").addClass("show");
            $("#exampleModal").css("display", "block");
            $(".custom-alert").show();
            $("#alerttext").text(data.message);
            $("#alerttext").css("color", "black");
            $(".custom-alert").css("background-color", "#45ffca");
            var borderElement = $(".custom-alert-border");
            borderElement.css("width", "100%");
            borderElement.animate(
              {
                width: 0,
              },
              function () {
                setTimeout(function () {
                  $(".custom-alert").hide();
                }, 1400);
              }
            );
          }
        },
        error: function (error) {},
      });
    });
    var otp = "";
    $('.otp-field input[type="number"]').on("keyup", function () {
      var inputValues = [];
      $('.otp-field input[type="number"]').each(function () {
        inputValues.push($(this).val());
      });
      otp = inputValues.join("");
    });

    $(".verify").click(function (e) {
      email = $("#email").val();
      newpassword = $("#matchfirst").val();
      var csrfToken = $('input[name="csrfmiddlewaretoken"]').val(); // Fetch the CSRF token from the page
      var Data = {
        email: email,
        newpassword: newpassword,
        otp: otp,
        csrfmiddlewaretoken: csrfToken,
      };
      e.preventDefault();
      if ($(".otpfield").val() != "" && $("#matchfirst").val() != "") {
        var newpasswordlength = $("#matchfirst").val();
        if (newpasswordlength.length >= 5) {
          $.ajax({
            url: "/forgotpassword/",
            type: "POST",
            data: Data,
            dataType: "json",
            beforeSend: function (xhr, settings) {
              xhr.setRequestHeader("X-CSRFToken", Data.csrfmiddlewaretoken);
            },
            success: function (data) {
              if (data.message === true) {
                $(".custom-alert").show();
                $("#alerttext").text("Password updated successfully.");
                $("#alerttext").css("color", "black");
                $(".custom-alert").css("background-color", "#45ffca");
                var borderElement = $(".custom-alert-border");
                borderElement.css("width", "100%");
                borderElement.animate({ width: 0 }, function () {
                  setTimeout(function () {
                    $(".custom-alert").hide();
                    window.location.reload();
                  }, 1400);
                });
              } else if (data.message == 2) {
                $(".custom-alert").show();
                $("#alerttext").text("Incorrect OTP");
                $("#alerttext").css("color", "white");
                $(".custom-alert").css("background-color", "#860A35");
                var borderElement = $(".custom-alert-border");
                borderElement.css("width", "100%");
                borderElement.animate({ width: 0 }, function () {
                  setTimeout(function () {
                    $(".custom-alert").hide();
                  }, 1400);
                });
              } else {
                $(".custom-alert").show();
                $("#alerttext").text(data.message);
                $("#alerttext").css("color", "black");
                $(".custom-alert").css("background-color", "#45ffca");
                var borderElement = $(".custom-alert-border");
                borderElement.css("width", "100%");
                borderElement.animate({ width: 0 }, function () {
                  setTimeout(function () {
                    $(".custom-alert").hide();
                  }, 1400);
                });
              }
            },
            error: function (error) {},
          });
        } else {
          $(".custom-alert").show();
          $("#alerttext").text("Password is too short");
          $("#alerttext").css("color", "white");
          $(".custom-alert").css("background-color", "#860A35");
          var borderElement = $(".custom-alert-border");
          borderElement.css("width", "100%");
          borderElement.animate({ width: 0 }, function () {
            setTimeout(function () {
              $(".custom-alert").hide();
            }, 1400);
          });
        }
      } else {
        $(".custom-alert").show();
        $("#alerttext").text("Please fill the form");
        $("#alerttext").css("color", "white");
        $(".custom-alert").css("background-color", "#860A35");
        var borderElement = $(".custom-alert-border");
        borderElement.css("width", "100%");
        borderElement.animate({ width: 0 }, function () {
          setTimeout(function () {
            $(".custom-alert").hide();
          }, 1400);
        });
      }
    });
  });
  // for signup

  $("#myForm").on("submit", function (event) {
    event.preventDefault(); // Prevent the default form submission
    check = checkingvalidation();
    var formData = {
      firstname: $("#firstname").val(),
      lastname: $("#lastname").val(),
      email: $("#email").val(),
      password: $("#password").val(),
      csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(), // Include CSRF token
    };
    if (check != false) {
      $("#signupButton").text("Please Wait");
      $.ajax({
        url: "/signup/",
        type: "POST",
        data: formData,
        dataType: "json",
        beforeSend: function (xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken", formData.csrfmiddlewaretoken);
        },
        success: function (data) {
          $("#signupButton").text("Signup");
          if (data.message == true) {
            $(".custom-alert").show();
            $("#alerttext").text("signup link successfully sent to your gmail");
            $("#alerttext").css("color", "black");

            $(".custom-alert").css("background-color", "#45ffca");
            var borderElement = $(".custom-alert-border");
            borderElement.css("width", "100%");
            borderElement.animate({ width: 0 }, function () {
              setTimeout(function () {
                $(".custom-alert").hide();
                // window.location.href='/';
              }, 5000);
            });
          } else {
            $(".custom-alert").show();
            $("#alerttext").text("user already registerd with this email");
            $("#alerttext").css("color", "white");
            $(".custom-alert").css("background-color", "#860A35");
            var borderElement = $(".custom-alert-border");
            borderElement.css("width", "100%");
            borderElement.animate({ width: 0 }, function () {
              setTimeout(function () {
                $(".custom-alert").hide();
              }, 1400);
            });
          }
        },
        error: function (error) {
          $("#signupButton").text("Signup");
          $(".custom-alert").show();
          $("#alerttext").text(
            "There was a problem with this account, please reload this page."
          );
          $("#alerttext").css("color", "white");
          $(".custom-alert").css("background-color", "#860A35");
          var borderElement = $(".custom-alert-border");
          borderElement.css("width", "100%");
          borderElement.animate({ width: 0 }, function () {
            setTimeout(function () {
              $(".custom-alert").hide();
            }, 1400);
          });
        },
      });
    } else {
      $(".custom-alert").show();
      $("#alerttext").text(message);
      $("#alerttext").css("color", "white");
      $(".custom-alert").css("background-color", "#860A35");
      var borderElement = $(".custom-alert-border");
      borderElement.css("width", "100%");
      borderElement.animate({ width: 0 }, function () {
        setTimeout(function () {
          $(".custom-alert").hide();
        }, 1400);
      });
    }
  });
  // send comment

  $("#commentform").on("submit", function (e) {
    console.log("commentform");
    e.preventDefault(); // Prevent the default form submission
    var commentText = $("#commentContent").val(); // Get comment text
    console.log(commentText);
    var articleId = $("#articleslug").val(); // Replace with the article ID
    $.ajax({
      type: "POST",
      url: "/sendcomment/", // Replace with your Django URL
      data: {
        comment: commentText,
        article_id: articleId,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      success: function (response) {
        $(".comments-list").append(
          '<div class="media p-4 mt-4">' +
            '<img src="https://via.placeholder.com/50" class="mr-3 rounded-circle" alt="User Avatar">' +
            '<div class="media-body">' +
            '<h5 class="mt-0">' +
            userName +
            "</h5>" +
            "<p>" +
            commentText +
            "</p>" +
            "</div>" +
            "</div>"
        );
        console.log(response);
        // Refresh the page or update comments section as needed
      },
      error: function (error) {
        // Handle error
        console.error("Error:", error);
      },
    });
  });

  // comment sending

  // contact us form
  $("#contactusform").on("submit", function (e) {
    e.preventDefault(); // Prevent the default form submission
    var fullname = $("#fullName").val(); // Get comment text
    var email = $("#email").val(); 
    var massage = $("#message").val();

    if (fullname!=""&&email!=""&&massage!=""){
      $.ajax({
        type: "POST",
        url: "/contact/", // Replace with your Django URL
        data: {
          fullname: fullname,
          email: email,
          massage: massage,
          csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        success: function (response) {
          $(".custom-alert").show();
          $("#alerttext").text(response.message);
          $("#alerttext").css("color", "black");
          $(".custom-alert").css("background-color", "#45FFCA");
          var borderElement = $(".custom-alert-border");
          borderElement.css("width", "100%");
          borderElement.animate({ width: 0 }, function () {
          setTimeout(function () {
          $(".custom-alert").hide();
          window.location.reload();
        }, 1400);
        });
          // Refresh the page or update comments section as needed
        },
        error: function (error) {
          // Handle error
          console.error("Error:", error);
        },
      });
    }
    else{
      $(".custom-alert").show();
      $("#alerttext").text("Please fill the form");
      $("#alerttext").css("color", "white");
      $(".custom-alert").css("background-color", "#860A35");
      var borderElement = $(".custom-alert-border");
      borderElement.css("width", "100%");
      borderElement.animate({ width: 0 }, function () {
        setTimeout(function () {
          $(".custom-alert").hide();
        }, 1400);
      });
    }
   
  });
  checkingvalidation();
});
