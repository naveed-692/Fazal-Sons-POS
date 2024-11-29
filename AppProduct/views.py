from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from django.http import Http404
from rest_framework import generics
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
    BaseAuthentication,
)
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db import connections
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from AppCustomer.utils import DistinctFetchAll
from django.db.models import Prefetch

# def DistinctFetchAll(cursor):
#     "Returns all rows from a cursor as a dict"
#     desc = cursor.description
#     return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]



### FUNCTION THAT CREATE TOKEN WHEN USER IS CREATED
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


### PAGINATION CLASS
class MyLimitOffsetPagination(LimitOffsetPagination):
    limit_query_param = "limit"
    offset_query_param = "Starting"


### OUTLET VIEW
class AddOutletView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Outlet.objects.all().order_by("outlet_name")
    serializer_class = OutletSerializer
    pagination_class = None


class OutletGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Outlet.objects.all().order_by("outlet_name")
    serializer_class = OutletSerializer
    pagination_class = None


@api_view(["GET"])
def FetchOutletView(request):
    outlet = Outlet.objects.all().values("outlet_name", "outlet_code")
    if len(outlet) > 0:
        serializer = OutletSerializer(outlet, many=True)
        param = {
            "status": 200,
            "results": serializer.data,
        }
        return Response(param)
    return Response(status=status.HTTP_204_NO_CONTENT)


### BRAND VIEW
class AddBrandView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Brand.objects.all().order_by("brand_name")
    serializer_class = BrandSerializer
    pagination_class = MyLimitOffsetPagination


class BrandGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all().order_by("brand_name")
    serializer_class = BrandSerializer


@api_view(["GET"])
def SearchBrandView(request, code):
    brand_name = code
    brand = Brand.objects.filter(brand_name__icontains=brand_name).order_by(
        "brand_name"
    )
    if len(brand) > 0:
        serializer = BrandSerializer(brand, many=True)
        param = {
            "status": 200,
            "results": serializer.data,
        }
        return Response(param)
    return Response(status=status.HTTP_204_NO_CONTENT)

### ATTRIBUTES TYPE VIEW
class AddAttributeTypeView(generics.ListCreateAPIView):
    queryset = AttributeType.objects.all().order_by("att_type")
    serializer_class = AttributeTypeSerializer
    pagination_class = None


class AttributeTypeGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttributeType.objects.all().order_by("att_type")
    serializer_class = AttributeTypeSerializer
    pagination_class = None


# ### ATTRIBUTES VIEW
# class AddAttributeView(generics.ListCreateAPIView):
#     queryset = Attribute.objects.all()
#     serializer_class = AttributeSerializer
#     pagination_class = None
#
#
# class AttributeGetView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Attribute.objects.all()
#     serializer_class = AttributeSerializer
#     pagination_class = None


## VARIATION VIEW
# class AddVariationView(generics.ListCreateAPIView):
#     queryset = Variation.objects.all()
#     serializer_class = VariationSerializer
#     pagination_class = None


# @api_view(['GET', 'POST'])
# def AddVariationView(request):
#     if request.method == 'GET':
#         cursor = connections['default'].cursor()
#         query_variation = "SELECT vr.id ,variation_name, vr.symbol, vr.description, attribute_name, vr.status FROM tbl_variation vr INNER JOIN tbl_attribute at on vr.attribute_name_id = at.id"
#         cursor.execute(query_variation)
#         variation = DistinctFetchAll(cursor)
#         serializer = VariationSerializer(variation, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = VariationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status='status.HTTP_201_CREATED')
#         return Response(serializer.errors, status='status.HTTP_400_BAD_REQUEST')
#
#
# class VariationGetView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Variation.objects.all()
#     serializer_class = VariationSerializer
#     pagination_class = None


### HEAD CATEGORY VIEW
class AddHeadCategoryView(generics.ListCreateAPIView):
    queryset = HeadCategory.objects.all().order_by("hc_name")
    serializer_class = HeadCategorySerializer
    pagination_class = None


class HeadCategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HeadCategory.objects.all().order_by("hc_name")
    serializer_class = HeadCategorySerializer
    pagination_class = None


### PARENT CATEGORY VIEW
class AddParentCategoryView(generics.ListCreateAPIView):
    queryset = ParentCategory.objects.all().order_by("pc_name")
    serializer_class = ParentCategorySerializer
    pagination_class = None


class ParentCategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParentCategory.objects.all().order_by("pc_name")
    serializer_class = ParentCategorySerializer
    pagination_class = None


### CATEGORY VIEW
class AddCategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by("category_name")
    serializer_class = CategorySerializer
    pagination_class = None


class CategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all().order_by("category_name")
    serializer_class = CategorySerializer
    pagination_class = None


### SUB CATEGORY VIEW
class AddSubCategoryView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all().order_by("sub_category_name")
    serializer_class = SubCategorySerializer
    pagination_class = None


class SubCategoryGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubCategory.objects.all().order_by("sub_category_name")
    serializer_class = SubCategorySerializer
    pagination_class = None


### TEMPORARY PRODUCT VIEW
class AddTemporaryProductView(generics.ListCreateAPIView):
    # parser_classes = [MultiPartParser, FormParser]
    queryset = TemporaryProduct.objects.all().order_by("product_name")
    serializer_class = TempProductSerializer
    pagination_class = None


class TemporaryProductGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TemporaryProduct.objects.all().order_by("product_name")
    serializer_class = TempProductSerializer
    pagination_class = None


### PRODUCT VIEW
class AddProduct(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by("product_name")
    serializer_class = ProductSerializer
    pagination_class = None


class ProductGetView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all().order_by("product_name")
    serializer_class = ProductSerializer
    pagination_class = None

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_stock = Stock.objects.filter(
            product_name=instance.product_name, sku=instance.sku
        )
        delete_stock.delete()
        self.perform_destroy(instance)
        return Response(status="200")


### FETCH ALL VARIATION ACCORDING TO ATTRIBUTE AND ITS TYPES VIEW
@api_view(["GET"])
def FetchAllAttributeTypeView(request):
    cursor = connections["default"].cursor()
    query = "SELECT att_type from tbl_attribute_type"
    cursor.execute(query)
    all_attribute_type = DistinctFetchAll(cursor)
    return Response(all_attribute_type)


@api_view(["GET"])
def FetchAttributeView(request, code):
    cursor = connections["default"].cursor()
    query = (
        "select attribute_name from tbl_attribute where att_type_id = '" + code + "'"
    )
    cursor.execute(query)
    fetch_attribute = DistinctFetchAll(cursor)
    return Response(fetch_attribute)


@api_view(["GET"])
def FetchVariationView(request, code):
    cursor = connections["default"].cursor()
    query_employee = (
        "SELECT variation_name, symbol FROM tbl_variation where attribute_name_id = '"
        + code
        + "'"
    )
    cursor.execute(query_employee)
    employee_location = DistinctFetchAll(cursor)
    return Response(employee_location)


### FETCH ALL PRODUCT NAME WITH OUTLET CODE AND STOCK VIEW
@api_view(["GET"])
def GetAllProductView(request):
    cursor = connections["default"].cursor()
    query_employee = "select distinct outlet_code ||'--' ||product_name as product_name, product_name as product_code  from tbl_product pr INNER JOIN tbl_outlet ot on pr.outlet_name_id = ot.outlet_name "
    cursor.execute(query_employee)
    product_name = DistinctFetchAll(cursor)
    return Response(product_name)


### FETCH ALL PRODUCT NAME WITH OUTLET CODE AND STOCK VIEW
@api_view(["GET"])
def FetchParentCategoryView(request, code):
    p_category = ParentCategory.objects.filter(hc_name_id=code)
    serializer = ParentCategorySerializer(p_category, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def FetchCategoryView(request, code):
    category = Category.objects.filter(pc_name_id=code)
    category_array = []
    if len(category) > 0:
        for i in range(len(category)):
            category_dict = dict()
            category_dict["id"] = category[i].id
            category_dict["category_name"] = category[i].category_name
            category_dict["symbol"] = category[i].symbol
            category_dict["description"] = category[i].description
            category_dict["status"] = category[i].status
            category_dict["pc_name"] = category[i].pc_name_id
            category_array.append(category_dict)
    return Response(category_array)


@api_view(["GET"])
def FetchSubCategoryView(request, code):
    sub_category = SubCategory.objects.filter(category_id=code)
    sub_category_array = []
    if len(sub_category) > 0:
        for i in range(len(sub_category)):
            sub_category_dict = dict()
            sub_category_dict["id"] = sub_category[i].id
            sub_category_dict["sub_category_name"] = sub_category[i].sub_category_name
            sub_category_dict["symbol"] = sub_category[i].symbol
            sub_category_dict["description"] = sub_category[i].description
            sub_category_dict["status"] = sub_category[i].status
            sub_category_dict["category"] = sub_category[i].category_id
            sub_category_array.append(sub_category_dict)
    return Response(sub_category_array)


@api_view(["GET", "POST"])
def AddVariationGroupView(request):
    if request.method == "GET":
        array = []
        attribute_type = AttributeType.objects.all()
        for i in range(len(attribute_type)):
            att_type = attribute_type[i].att_type
            att_type_id = attribute_type[i].id

            attribute = Attribute.objects.filter(att_type_id=att_type_id)
            if len(attribute) > 0:
                for i in range(len(attribute)):
                    att_name = attribute[i].attribute_name
                    att_id = attribute[i].id
                    attribute_name_id = attribute[i].id

                    variation = Variation.objects.filter(
                        attribute_name=attribute_name_id
                    )
                    if len(variation) > 0:
                        variation_name = []
                        for i in range(len(variation)):
                            variation_name.append(variation[i].variation_name)
                        Dict = dict()
                        Dict["att_id"] = att_id
                        Dict["att_type"] = att_type
                        Dict["attribute_name"] = att_name
                        Dict["variation"] = variation_name
                        array.append(Dict)
                    elif len(variation) == 0:
                        Dict = dict()
                        Dict["att_id"] = att_id
                        Dict["att_type"] = att_type
                        Dict["attribute_name"] = att_name
                        Dict["variation"] = None
                        array.append(Dict)
        return Response(array)
    if request.method == "POST":
        data = request.data
        for i in range(len(data)):
            serializer = VariationGroupSerializer(data=request.data[i])
            if serializer.is_valid():
                serializer.save()
        return Response(data, status="200")


@api_view(["GET", "PUT", "DELETE"])
def GetVariationGroupView(request, att_id):
    if request.method == "GET":
        array = []
        try:
            attribute = Attribute.objects.get(id=att_id)
            attribute_type = AttributeType.objects.get(id=attribute.att_type_id)
        except:
            return Response("NO RECORD FOUND")
        att_type = attribute_type.att_type
        att_type_id = attribute_type.id
        att_name = attribute.attribute_name
        attribute_name_id = attribute.id

        variation = Variation.objects.filter(attribute_name=attribute_name_id)
        if len(variation) > 0:
            variation_name = []
            for i in range(len(variation)):
                variation_name.append(variation[i].variation_name)
            Dict = dict()
            Dict["att_id"] = att_id
            Dict["att_type"] = att_type
            Dict["attribute_name"] = att_name
            Dict["variation_name"] = variation_name
            array.append(Dict)
        elif len(variation) == 0:
            Dict = dict()
            Dict["att_id"] = att_id
            Dict["att_type"] = att_type
            Dict["attribute_name"] = att_name
            Dict["variation_name"] = None
            array.append(Dict)
        return Response(array)
    elif request.method == "PUT":

        data = request.data
        id = data["att_id"]
        try:
            attribute = Attribute.objects.get(id=id)
        except:
            return Response("NO RECORD FOUND")

        attribute.attribute_name = data["attribute_name"]
        attribute.att_type_id = data["att_type"]
        attribute.save()

        variation = Variation.objects.filter(attribute_name=att_id)
        if len(variation) == len(data["variation_name"]):
            for i in range(len(variation)):
                variation[i].variation_name = data["variation_name"][i]
                variation[i].save()
        elif len(variation) != len(data["variation_name"]):
            if len(variation) > 0:
                for i in range(len(variation)):
                    variation[i].delete()
                for y in range(len(data["variation_name"])):
                    variation = Variation()
                    variation.variation_name = data["variation_name"][y]
                    variation.attribute_name_id = data["att_id"]
                    variation.status = "active"
                    variation.created_at = datetime.datetime.now()
                    variation.save()
            else:
                for y in range(len(data["variation_name"])):
                    variation = Variation()
                    variation.variation_name = data["variation_name"][y]
                    variation.attribute_name_id = data["att_id"]
                    variation.status = "active"
                    variation.created_at = datetime.datetime.now()
                    variation.save()
        return Response(data)
    elif request.method == "DELETE":
        attribute = Attribute.objects.get(id=att_id)
        variation = Variation.objects.filter(attribute_name_id=att_id)
        for i in range(len(variation)):
            variation[i].delete()
        attribute.delete()
        attribute_type = Attribute.objects.filter(att_type_id=attribute.att_type_id)
        if len(attribute_type) == 0:
            attribute_type = AttributeType.objects.get(id=attribute.att_type_id)
            attribute_type.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def FetchVariationGroupView(request, att_typ_id):
    if request.method == "GET":
        att_id = att_typ_id
        array = []
        try:
            attribute_type = AttributeType.objects.get(id=att_id)
            attribute = Attribute.objects.filter(att_type=attribute_type.id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        for i in range(len(attribute)):
            att_type = attribute_type.att_type
            att_type_id = attribute_type.id
            att_name = attribute[i].attribute_name
            attribute_id = attribute[i].id
            attribute_name_id = attribute[i].id

            variation = Variation.objects.filter(attribute_name=attribute_name_id)
            if len(variation) > 0:
                variation_name = []
                for i in range(len(variation)):
                    variation_name.append(variation[i].variation_name)
                Dict = dict()
                Dict["att_id"] = att_id
                Dict["att_type"] = att_type
                Dict["attribute_name"] = att_name
                Dict["attribute_id"] = attribute_id
                Dict["variation"] = variation_name
                array.append(Dict)
            elif len(variation) == 0:
                Dict = dict()
                Dict["att_id"] = att_id
                Dict["att_type"] = att_type
                Dict["attribute_name"] = att_name
                Dict["attribute_id"] = attribute_id
                Dict["variation"] = None
                array.append(Dict)
        return Response(array)


@api_view(["GET", "POST"])
def AddCategoriesView(request):
    if request.method == "GET":
        cursor = connections["default"].cursor()
        query = "Select ca.id, category_name, ca.symbol, subcategory_option, ca.description, ca.status, pc_name from tbl_category ca inner join tbl_parent_category pc on ca.pc_name_id = pc.id"
        cursor.execute(query)
        variation_group = DistinctFetchAll(cursor)
        variation_array = []
        if len(variation_group) > 0:
            for i in range(len(variation_group)):
                variation_dict = dict()
                variation_dict["id"] = variation_group[i]["id"]
                variation_dict["category_name"] = variation_group[i]["category_name"]
                variation_dict["symbol"] = variation_group[i]["symbol"]
                variation_dict["subcategory_option"] = variation_group[i][
                    "subcategory_option"
                ]
                variation_dict["description"] = variation_group[i]["description"]
                variation_dict["status"] = variation_group[i]["status"]
                variation_dict["pc_name"] = variation_group[i]["pc_name"]
                category_attribute = CategoryAttribute.objects.filter(
                    category_id=variation_group[i]["id"]
                )
                attribute_group_array = []
                if len(category_attribute) > 0:
                    for i in range(len(category_attribute)):
                        attribute = Attribute.objects.get(
                            id=category_attribute[i].attribute_id
                        ).attribute_name
                        attribute_group_array.append(attribute)
                variation_dict["attribute_group"] = attribute_group_array
                variation_array.append(variation_dict)
        return Response(variation_array)

    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            category_array = []
            category_dict = dict()
            category_name = request.data["category_name"].strip()
            category = Category.objects.get(category_name=category_name)
            category_dict["id"] = category.id
            category_dict["pc_name"] = category.pc_name_id
            category_dict["category_name"] = category.category_name
            category_dict["symbol"] = category.symbol
            category_dict["description"] = category.description
            category_dict["status"] = category.status
            attribute_group_array = []
            category_attribute = CategoryAttribute.objects.filter(
                category_id=category.id
            )
            if len(category_attribute) > 0:
                for i in range(len(category_attribute)):
                    attribute = Attribute.objects.get(
                        id=category_attribute[i].attribute_id
                    ).attribute_name
                    attribute_group_array.append(attribute)
            category_dict["attribute_group"] = attribute_group_array
            category_array.append(category_dict)
            return Response(category_array)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def GetCategoriesView(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        cursor = connections["default"].cursor()
        # query = (
        #     "Select ca.id, category_name, ca.symbol, subcategory_option, ca.description, ca.status, pc_name from tbl_category ca inner join tbl_parent_category pc on ca.pc_name_id = pc.id where ca.id = '"
        #     + id
        #     + "'"
        # )
        query = (
            "Select ca.id, category_name, ca.symbol, subcategory_option, ca.description, ca.status, pc_name, pc.id as parent_id, hc.id as head_id, hc_name as head_name, pc_name as parent_name from tbl_category ca inner join tbl_parent_category pc on ca.pc_name_id = pc.id inner join tbl_head_category hc on pc.hc_name_id = hc.id where ca.id = '"+ id +"'"
        )
        cursor.execute(query)
        variation_group = DistinctFetchAll(cursor)

        if len(variation_group) > 0:
            variation_array = []
            for i in range(len(variation_group)):
                variation_dict = dict()
                variation_dict["id"] = variation_group[i]["id"]
                variation_dict["head_id"] = variation_group[i]["head_id"]
                variation_dict["head_name"] = variation_group[i]["head_name"]
                variation_dict["parent_id"] = variation_group[i]["parent_id"]
                variation_dict["parent_name"] = variation_group[i]["parent_name"]
                variation_dict["category_name"] = variation_group[i]["category_name"]
                variation_dict["symbol"] = variation_group[i]["symbol"]
                variation_dict["subcategory_option"] = variation_group[i][
                    "subcategory_option"
                ]
                variation_dict["description"] = variation_group[i]["description"]
                variation_dict["status"] = variation_group[i]["status"]
                variation_dict["pc_name"] = variation_group[i]["pc_name"]
                category_attribute = CategoryAttribute.objects.filter(category_id=id)
                attribute_group_array = []
                attribute_type_array = []
                if len(category_attribute) > 0:
                    for i in range(len(category_attribute)):
                        attribute = Attribute.objects.get(
                            id=category_attribute[i].attribute_id
                        )
                        attribute_group_array.append(attribute.attribute_name)
                        attribute_type_array.append(attribute.att_type_id)
                variation_dict["attribute_group"] = attribute_group_array
                variation_dict["att_type"] = attribute_type_array
                variation_array.append(variation_dict)
        return Response(variation_array)

    elif request.method == "PUT":
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.initial_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def FetchCategoriesView(request, id):
    if request.method == "GET":
        try:
            category = Category.objects.get(id=id)
        except Category.DoesNotExist:
                 return Response(status=status.HTTP_404_NOT_FOUND)

        category_attribute = CategoryAttribute.objects.filter(category_id=category.id)
        cat_array = []
        if len(category_attribute) > 0:
            for i in range(len(category_attribute)):
                try:
                    attribute = Attribute.objects.get(
                        id=category_attribute[i].attribute_id
                    )
                except:
                    return Response("Attribute not found against this category")

                variation = Variation.objects.filter(attribute_name_id=attribute.id)
                if len(variation) > 0:
                    cat_dict = dict()
                    cat_dict["id"] = category.id
                    cat_dict["category"] = category.category_name
                    cat_dict["attribute"] = attribute.attribute_name
                    variation_array = []
                    for x in range(len(variation)):
                        variation_array.append(variation[x].variation_name)
                        cat_dict["variation"] = variation_array
                    cat_array.append(cat_dict)
        return Response(cat_array)

    #     att_id = att_typ_id
    #     array = []
    #     try:
    #     #     attribute_type = AttributeType.objects.get(id=att_id)
    #     #     attribute = Attribute.objects.filter(att_type=attribute_type.id)
    #     # except:
    #     #     return Response("NO RECORD FOUND")
    #     # for i in range(len(attribute)):
    #     #     att_type = attribute_type.att_type
    #     #     att_type_id = attribute_type.id
    #     #     att_name = attribute[i].attribute_name
    #     #     attribute_name_id = attribute[i].id
    #     #
    #     #     variation = Variation.objects.filter(attribute_name=attribute_name_id)
    #     #     if len(variation) > 0:
    #     #         variation_name = []
    #     #         for i in range(len(variation)):
    #     #             variation_name.append(variation[i].variation_name)
    #     #         Dict = dict()
    #     #         Dict['att_id'] = att_id
    #     #         Dict['att_type'] = att_type
    #     #         Dict['attribute_name'] = att_name
    #     #         Dict['variation'] = variation_name
    #     #         array.append(Dict)
    #     #     elif len(variation) == 0:
    #     #         Dict = dict()
    #     #         Dict['att_id'] = att_id
    #     #         Dict['att_type'] = att_type
    #     #         Dict['attribute_name'] = att_name
    #     #         Dict['variation'] = None
    #     #         array.append(Dict)
    #     # return Response(array)


# from rest_framework.views import APIView
#
#
# class ImageUploadView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = ImageModelSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET", "POST"])
# def AddSubCategoriesView(request):
#     if request.method == "GET":
#         # Use select_related and prefetch_related to optimize queries
#         sub_categories = SubCategory.objects.select_related('category').prefetch_related(
#             Prefetch(
#                 'subcategoryattribute_set',  # Adjust based on your related name
#                 queryset=SubCategoryAttribute.objects.select_related('attribute')
#             )
#         )

#         sub_category_array = []
#         for sub_category in sub_categories:
#             sub_category_dict = {
#                 "id": sub_category.id,
#                 "sub_category_name": sub_category.sub_category_name,
#                 "symbol": sub_category.symbol,
#                 "description": sub_category.description,
#                 "status": sub_category.status,
#                 "category": sub_category.category.category_name if sub_category.category else None,
#                 "attribute_group": [
#                     attribute.attribute.attribute_name
#                     for attribute in sub_category.subcategoryattribute_set.all()
#                 ],
#             }
#             sub_category_array.append(sub_category_dict)

#         return Response(sub_category_array)

#     elif request.method == "POST":
#         serializer = SubCategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             sub_category = serializer.instance  # Access the saved instance directly
#             sub_category_dict = {
#                 "id": sub_category.id,
#                 "category": sub_category.category_id,
#                 "sub_category_name": sub_category.sub_category_name,
#                 "symbol": sub_category.symbol,
#                 "description": sub_category.description,
#                 "status": sub_category.status,
#                 "attribute_group": [
#                     attr.attribute.attribute_name
#                     for attr in sub_category.subcategoryattribute_set.all()
#                 ],
#             }
#             return Response(sub_category_dict, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(["GET", "POST"])
def AddSubCategoriesView(request):
    if request.method == "GET":
        sub_category = SubCategory.objects.all()
        sub_category_array = []
        if len(sub_category) > 0:
            for i in range(len(sub_category)):
                sub_category_dict = dict()
                sub_category_dict["id"] = sub_category[i].id
                sub_category_dict["sub_category_name"] = sub_category[
                    i
                ].sub_category_name
                sub_category_dict["symbol"] = sub_category[i].symbol
                sub_category_dict["description"] = sub_category[i].description
                sub_category_dict["status"] = sub_category[i].status

                if  sub_category[i].category_id != None:
                    sub_category_dict["category"] = sub_category[i].category.category_name
                else:
                    sub_category_dict["category"] = None

                sub_category_attribute = SubCategoryAttribute.objects.filter(
                    sub_category_id=sub_category[i].id
                )
                attribute_group_array = []
                if len(sub_category_attribute) > 0:
                    for i in range(len(sub_category_attribute)):
                        attribute = Attribute.objects.get(
                            id=sub_category_attribute[i].attribute_id
                        ).attribute_name
                        attribute_group_array.append(attribute)
                sub_category_dict["attribute_group"] = attribute_group_array
                sub_category_array.append(sub_category_dict)
        return Response(sub_category_array)
    elif request.method == "POST":
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sub_category_array = []
            sub_category_dict = dict()
            sub_category_name = request.data["sub_category_name"].strip()
            sub_category = SubCategory.objects.get(sub_category_name=sub_category_name)
            sub_category_dict["id"] = sub_category.id
            sub_category_dict["category"] = sub_category.category_id
            sub_category_dict["sub_category_name"] = sub_category.sub_category_name
            sub_category_dict["symbol"] = sub_category.symbol
            sub_category_dict["description"] = sub_category.description
            sub_category_dict["status"] = sub_category.status
            attribute_group_array = []
            sub_category_attribute = SubCategoryAttribute.objects.filter(
                sub_category_id=sub_category.id
            )
            if len(sub_category_attribute) > 0:
                for i in range(len(sub_category_attribute)):
                    attribute = Attribute.objects.get(
                        id=sub_category_attribute[i].attribute_id
                    ).attribute_name
                    attribute_group_array.append(attribute)
            sub_category_dict["attribute_group"] = attribute_group_array
            sub_category_array.append(sub_category_dict)
            return Response(sub_category_array)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def GetSubCategoriesView(request, id):
    try:
        sub_category = SubCategory.objects.get(id=id)
    except SubCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        sub_category_array = []
        sub_category_dict = dict()
        sub_category_dict["id"] = sub_category.id
        sub_category_dict["sub_category_name"] = sub_category.sub_category_name
        sub_category_dict["symbol"] = sub_category.symbol
        sub_category_dict["description"] = sub_category.description
        sub_category_dict["status"] = sub_category.status
        sub_category_dict["category"] = sub_category.category.category_name
        sub_category_attribute = SubCategoryAttribute.objects.filter(
            sub_category_id=sub_category.id
        )
        attribute_group_array = []
        if len(sub_category_attribute) > 0:
            for i in range(len(sub_category_attribute)):
                attribute = Attribute.objects.get(
                    id=sub_category_attribute[i].attribute_id
                ).attribute_name
                attribute_group_array.append(attribute)
        sub_category_dict["attribute_group"] = attribute_group_array
        sub_category_array.append(sub_category_dict)
        return Response(sub_category_array, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        serializer = SubCategorySerializer(sub_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.initial_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        sub_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["Get"])
# def FetchSubCategoriesView(request , id):
#       if request.method == "GET":
#         try:
#             sub_category = SubCategory.objects.get(id=id)
#         except SubCategory.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         sub_category_attribute = SubCategoryAttribute.objects.filter(sub_category_id=sub_category.id)
#         sub_cat_array = []
#         if len(sub_category_attribute) > 0:
#             for i in range(len(sub_category_attribute)):
#                 try:
#                     attribute = Attribute.objects.get(
#                         id=sub_category_attribute[i].attribute_id
#                     )
#                 except:
#                     return Response(status=status.HTTP_404_NOT_FOUND)

#                 variation = Variation.objects.filter(attribute_name_id=attribute.id)
#                 if len(variation) > 0:
#                     sub_cat_dict = dict()
#                     sub_cat_dict["id"] = sub_category.id
#                     sub_cat_dict["sub_category"] = sub_category.sub_category_name
#                     sub_cat_dict["attribute"] = attribute.attribute_name
#                     variation_array = []
#                     for x in range(len(variation)):
#                         variation_array.append(variation[x].variation_name)
#                         sub_cat_dict["variation"] = variation_array
#                     sub_cat_array.append(sub_cat_dict)
#         return Response(sub_cat_array)
    
    

@api_view(["GET"])
def FetchSubCategoriesView(request, id):
    try:
        # Fetch the subcategory by ID
        sub_category = SubCategory.objects.get(id=id)
    except SubCategory.DoesNotExist:
        return Response(
            {"error": "SubCategory with the given ID does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Fetch related SubCategoryAttributes and their associated Attributes and Variations
    sub_category_attributes = SubCategoryAttribute.objects.filter(sub_category_id=sub_category.id).select_related('attribute')
    response_data = []

    for sub_cat_attr in sub_category_attributes:
        attribute = sub_cat_attr.attribute
        if not attribute:
            continue

        # Fetch all variations for the attribute
        variations = Variation.objects.filter(attribute_name_id=attribute.id).values_list('variation_name', flat=True)

        # Prepare the response dictionary
        response_data.append({
            "id": sub_category.id,
            "sub_category": sub_category.sub_category_name,
            "attribute": attribute.attribute_name,
            "variation": list(variations),
        })

    # Return the response
    return Response(response_data, status=status.HTTP_200_OK)
