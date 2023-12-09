from django.db import models

# Create your models here.

class Article(models.Model):
    title = models.CharField(max_length=200)
    img_title = models.CharField(max_length=200)  # Assuming it's a CharField, adjust if needed
    slug = models.SlugField(max_length=300)
    img_alt = models.CharField(max_length=200)  # Assuming it's a CharField, adjust if needed
    tags = models.CharField(max_length=200)
    category_choice=[
        ('tech', 'Technology'),
        ('health', 'Health & Wellness'),
        ('fashion', 'Fashion & Beauty'),
        ('food', 'Food & Cooking'),
        ('lifestyle', 'Lifestyle'),
        ('finance', 'Finance & Business'),
        ('arts', 'Arts & Entertainment'),
        ('education', 'Education'),
        ('science', 'Science & Nature'),
    ]
    sub_category_choice=[
        ('Programming', 'Programming'),
        ('Web Development', 'Web Development'),
        ('Mobile Apps', 'Mobile Apps'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Data Science', 'Data Science'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Fitness', 'Fitness'),
        ('Nutrition', 'Nutrition'),
        ('Mental Health', 'Mental Health'),
        ('Yoga & Meditation', 'Yoga & Meditation'),
        ('Healthy Living', 'Healthy Living'),
        ('Destination Guides', 'Destination Guides'),
        ('Travel Tips', 'Travel Tips'),
        ('Adventure Travel', 'Adventure Travel'),
        ('Backpacking', 'Backpacking'),
        ('Solo Travel', 'Solo Travel'),
        ('Fashion Trends', 'Fashion Trends'),
        ('Beauty Tips', 'Beauty Tips'),
        ('Makeup Tutorials', 'Makeup Tutorials'),
        ('Clothing Styles', 'Clothing Styles'),
        ('Accessories', 'Accessories'),
        ('Recipes', 'Recipes'),
        ('Cooking Tips', 'Cooking Tips'),
        ('Restaurant Reviews', 'Restaurant Reviews'),
        ('Healthy Eating', 'Healthy Eating'),
        ('International Cuisine', 'International Cuisine'),
        ('Personal Development', 'Personal Development'),
        ('Productivity', 'Productivity'),
        ('Relationships', 'Relationships'),
        ('Self-Care', 'Self-Care'),
        ('Home & Decor', 'Home & Decor'),
        ('Personal Finance', 'Personal Finance'),
        ('Investing', 'Investing'),
        ('Entrepreneurship', 'Entrepreneurship'),
        ('Marketing', 'Marketing'),
        ('Career Development', 'Career Development'),
        ('Movie Reviews', 'Movie Reviews'),
        ('Book Recommendations', 'Book Recommendations'),
        ('Music & Concerts', 'Music & Concerts'),
        ('Art & Design', 'Art & Design'),
        ('Theater & Performance', 'Theater & Performance'),
        ('Learning Strategies', 'Learning Strategies'),
        ('Educational Technology', 'Educational Technology'),
        ('Study Tips', 'Study Tips'),
        ('Online Courses', 'Online Courses'),
        ('Career Advice', 'Career Advice'),
        ('Astronomy', 'Astronomy'),
        ('Biology', 'Biology'),
        ('Environmental Science', 'Environmental Science'),
        ('Physics', 'Physics'),
    ]
    category = models.CharField(max_length=100, choices=category_choice, default="NULL")
    sub_category =models.CharField(max_length=100, choices=sub_category_choice, default="NULL")
    thumbnail = models.ImageField(upload_to='Article/thumbnails/')
    short_description = models.TextField()
    main_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
