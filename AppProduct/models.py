from django.db import models

SEASONS_CHOICES = (
    ('Spring', 'Spring'),
    ('Summer', 'Summer'),
    ('Autumn', 'Autumn'),
    ('Winter', 'Winter'),
)

STATUS = (
    ('active', 'Active'),
    ('pending', 'Pending'),
    ('inactive', 'Inactive'),
)


# Create your models here.

class Brand(models.Model):
    brand_name = models.CharField(max_length=100, null=True, unique=True)
    symbol = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_brand'

    def __str__(self):
        return self.brand_name


class Attribute(models.Model):
    attribute_name = models.CharField(max_length=100, null=True, unique=True)
    type = models.CharField(max_length=100, null=True)
    symbol = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=500, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_attribute'

    def __str__(self):
        return self.attribute_name


class Variation(models.Model):
    vairation_name = models.CharField(max_length=100, null=True)
    attribute_name = models.ForeignKey(Attribute, to_field='attribute_name', on_delete=models.CASCADE, null=True)
    symbol = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=500, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'tbl_variation'

    def __str__(self):
        return self.vairation_name


class ParentCategory(models.Model):
    category_head = models.CharField(max_length=100, null=True)
    pc_name = models.CharField(max_length=100, null=True, unique=True)
    symbol = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=500, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_parent_category'

    def __str__(self):
        return self.pc_name


class Category(models.Model):
    pc_name = models.ForeignKey(ParentCategory, to_field='pc_name', on_delete=models.CASCADE, null=True)
    category_name = models.CharField(max_length=100, null=True, unique=True)
    symbol = models.CharField(max_length=100, null=True)
    subcategory_option = models.TextField(max_length=500, null=True)
    description = models.TextField(max_length=500, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_category'

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    category_name = models.ForeignKey(Category, to_field='category_name', on_delete=models.CASCADE, null=True)
    sub_category_name = models.CharField(max_length=100, null=True, unique=True)
    symbol = models.CharField(max_length=100, null=True)
    description = models.TextField(max_length=500, null=True)
    status = models.CharField(max_length=20, choices=STATUS, default='Active')
    attribute_name = models.ForeignKey(Attribute, to_field='attribute_name', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_sub_category'

    def __str__(self):
        return self.sub_category_name


class Product(models.Model):
    product_name = models.CharField(max_length=100, null=True)
    product_outlet = models.CharField(max_length=100, null=True)
    sku = models.CharField(max_length=100, null=True)
    head_category = models.CharField(max_length=100, null=True)
    pc_name = models.ForeignKey(ParentCategory, to_field='pc_name', on_delete=models.CASCADE, null=True)
    category_name = models.ForeignKey(Category, to_field='category_name', on_delete=models.CASCADE, null=True)
    sub_category_name = models.ForeignKey(SubCategory, to_field='sub_category_name', on_delete=models.CASCADE,
                                          null=True)
    brand_name = models.ForeignKey(Brand, to_field='brand_name', on_delete=models.CASCADE,
                                   null=True)
    season = models.CharField(max_length=10, choices=SEASONS_CHOICES, default='Spring')
    description = models.TextField(max_length=500, null=True)
    created_at = models.DateTimeField(null=True)
    created_by = models.CharField(max_length=200, null=True, blank=True)
    updated_at = models.DateTimeField(null=True)
    updated_by = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'tbl_product'

    def __str__(self):
        return self.product_name
