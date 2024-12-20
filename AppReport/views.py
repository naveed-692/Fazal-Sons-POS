from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import *

from rest_framework.decorators import api_view
from django.db import connections
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
import json
from AppPOS.models import *
from AppCustomer.utils import DistinctFetchAll
from django.db.models import Sum, FloatField
from django.db.models.functions import Cast




@api_view(['GET'])
def GetAllOutletDateView(request, outlet_code):
    cursor = connections['default'].cursor()
    query = "select distinct created_at::date from tbl_transaction where outlet_code_id = '" + outlet_code + "'"
    cursor.execute(query)
    daily_report = DistinctFetchAll(cursor)
    return Response(daily_report)



@api_view(['GET'])
def DailySaleView(request, outlet_code, date):
    try:
        print(outlet_code)
        print(date)
        cursor = connections['default'].cursor()
        # query = "select invoice_code , trans.created_at , ol.outlet_name , cus.customer_type_id as customer_type, sum(grand_total::INTEGER) as total from tbl_transaction as trans INNER JOIN tbl_customer as cus on cus.cust_code = trans.cust_code_id INNER JOIN tbl_outlet as ol on ol.id = trans.outlet_code_id where trans.created_at::date = '" + date + "' and ol.id = '" + outlet_code + "' GROUP BY  invoice_code , trans.created_at ,  ol.outlet_name,  cus.customer_type_id"
        query = "SELECT trans.invoice_code, trans.created_at, ol.outlet_name, cus.customer_type_id AS customer_type, SUM(trans.grand_total::INTEGER) AS total_amount, COALESCE(ret.total_return, 0) AS return_amount , SUM(trans.grand_total::INTEGER) - COALESCE(ret.total_return, 0) as total  FROM tbl_transaction AS trans INNER JOIN tbl_customer AS cus ON cus.cust_code = trans.cust_code_id INNER JOIN tbl_outlet AS ol ON ol.id = trans.outlet_code_id LEFT JOIN (SELECT invoice_code_id, SUM(total_amount::INTEGER) AS total_return FROM tbl_transaction_return GROUP BY invoice_code_id ) AS ret ON trans.invoice_code = ret.invoice_code_id WHERE trans.created_at::date = '"+ date +"' AND ol.id = '"+ outlet_code +"'GROUP BY trans.invoice_code, trans.created_at, ol.outlet_name, cus.customer_type_id, ret.total_return;"
        cursor.execute(query)
        daily_report = DistinctFetchAll(cursor)
        return Response(daily_report)
        return Response(daily_report if daily_report else [])
    except Exception as e:
             return Response({"error": str(e)}, status=500)


@api_view(['GET'])
def DailySaleDetailView(request, invoice_code):
    cursor = connections['default'].cursor()
    query = "select invoice_code, quantity, gross_total, discounted_value, items_discount, grand_total, payment_type, tr.status, customer_type_id , tr.created_at::date from tbl_transaction tr INNER JOIN tbl_customer cus on cus.cust_code = tr.cust_code_id  where invoice_code = '" + invoice_code + "'"
    cursor.execute(query)
    transaction = DistinctFetchAll(cursor)

    query_item = "select tr_item.quantity, rate as per_rate, tr_item.gross_total, tr_item.discounted_value, item_total  from tbl_transaction tr INNER JOIN tbl_transaction_item tr_item on tr.invoice_code = tr_item.invoice_code_id  where invoice_code = '" + invoice_code + "'"
    cursor.execute(query_item)
    transaction_item = DistinctFetchAll(cursor)
 

    data_dict = dict()
    if len(transaction) > 0:
        data_dict["customer_type"] = transaction[0]["customer_type_id"]
        data_dict["date"] = str(transaction[0]["created_at"])
        data_dict["gross_total"] = transaction[0]["gross_total"]
        data_dict["discount"] = transaction[0]["discounted_value"]
        data_dict["grand_total"] = transaction[0]["grand_total"]
        data_dict["status"] = transaction[0]["status"]
        data_dict["items"] = []

        for x in range(len(transaction_item)):
            data_dict["items"].append(transaction_item[x])
    return Response(data_dict)
 


@api_view(['GET'])
def SalesReportView(request, start_date, end_date):
    cursor = connections['default'].cursor()
    query = "select sum(grand_total::INTEGER) as total_sale, created_at::date as till_date from tbl_transaction  where created_at::date between '" + start_date + "' and '" + end_date + "' group by till_date order by  till_date DESC"
    cursor.execute(query)
    report = DistinctFetchAll(cursor)

    sales_report = []
    total = 0
    if len(report) > 0:
        for x in range(len(report)):
            data_dict = dict()
            data_dict["till_date"] = str(report[x]["till_date"])
            data_dict["total_sale"] = report[x]["total_sale"]
            total += int(report[x]["total_sale"])
            sales_report.append(data_dict)
        data_dict = dict()
        data_dict["total"] = total
        sales_report.append(data_dict)

    return Response(sales_report)



@api_view(['GET'])
def ProfitReportView(request, outlet_code, date):
    cursor = connections['default'].cursor()
    # query = "select invoice_code_id, tr_item.sku as sku, product_name, quantity, cost_price,  quantity::INTEGER*cost_price::INTEGER as total_cost , selling_price, quantity::INTEGER*selling_price::INTEGER as total ,quantity::INTEGER*selling_price::INTEGER -  quantity::INTEGER*cost_price::INTEGER as profit   from tbl_transaction_item tr_item INNER JOIN tbl_product pr on tr_item.sku = pr.sku"
    query = "select invoice_code, tr_item.sku as sku, product_name,tr.created_at, outlet_code_id, tr_item.quantity, cost_price,  tr_item.quantity::INTEGER*cost_price::INTEGER as total_cost , selling_price, tr_item.quantity::INTEGER*selling_price::INTEGER as total ,tr_item.quantity::INTEGER*selling_price::INTEGER -  tr_item.quantity::INTEGER*cost_price::INTEGER as profit from tbl_transaction_item tr_item INNER JOIN tbl_product pr on tr_item.sku = pr.sku inner join tbl_transaction tr on tr_item.invoice_code_id = tr.invoice_code where outlet_code_id ='"+ outlet_code +"' and tr.created_at::date = '"+ date +"' order by invoice_code"
    cursor.execute(query)
    report = DistinctFetchAll(cursor)

    profit_report = []
    TotalQuantity = 0
    TotalCost = 0
    Total = 0
    Profit = 0
    if len(report) > 0:
        for x in range(len(report)):
            data_dict = dict()
            data_dict["invoice_code"] = report[x]["invoice_code"]
            data_dict["sku"] = report[x]["sku"]
            data_dict["product_name"] = report[x]["product_name"]
            data_dict["quantity"] = report[x]["quantity"]
            data_dict["cost_price"] = report[x]["cost_price"]
            data_dict["total_cost"] = report[x]["total_cost"]
            data_dict["selling_price"] = report[x]["selling_price"]
            data_dict["total"] = report[x]["total"]
            data_dict["profit"] = report[x]["profit"]

            TotalQuantity += int(report[x]["quantity"])
            TotalCost += int(report[x]["total_cost"])
            Total += int(report[x]["total"])
            Profit += int(report[x]["profit"])
            profit_report.append(data_dict)

        data_dict = dict()
        data_dict["TotalQuantity"] = TotalQuantity
        data_dict["TotalCost"] = TotalCost
        data_dict["Total"] = Total
        data_dict["Profit"] = Profit
        profit_report.append(data_dict)

    return Response(profit_report)
  
