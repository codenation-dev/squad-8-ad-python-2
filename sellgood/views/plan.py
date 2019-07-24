import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from sellgood.models import Plan
from sellgood.forms import PlanForm


@csrf_exempt
def create_plan(request):  # Create Plan
    if request.method == 'POST':  # Check request method
        plan_data = json.loads(request.body)
        form = PlanForm(plan_data)
        if form.is_valid():  # Body request validation
            name = form.cleaned_data['name']
            minimum_amount = form.cleaned_data['minimum_amount']
            lower_percentage = form.cleaned_data['lower_percentage']
            higher_percentage = form.cleaned_data['higher_percentage']

            # Create a new plan
            new_plan = Plan.objects.create(
                name=name, minimum_amount=minimum_amount,
                lower_percentage=lower_percentage, higher_percentage=higher_percentage)

            # TODO: Que _ misterioso é esse depois de seller
            # Body content when form is valid.
            response_body = dict(name=new_plan.name)

            # Since body content is valid, return response_body
            return JsonResponse(response_body, status=200)

        # Since body not valid, return errors
        else:
            return JsonResponse(form.errors, status=422)

    else:  # If method is not POST return body_content
        body_content = {
            'error': 'Method not allowed'
        }
        return JsonResponse(body_content, status=405)


@csrf_exempt
def read_plan(request, id='NONE'):  # Read plans
    if request.method != 'GET':  # If method is not GET return error
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:  # If request method == GET
        if id =='NONE':  #  Return Plan List
            return JsonResponse({'sales': list(Plan.objects.all())}, status=200)

        else:  # Return the especifc plan
            plan = Plan.objects.filter(id=id).values('id', 'name', 'minimum_amount',
                                                               'lower_percentage', 'higher_percentage')

            if not plan:  # Return error if seller_id doesn't exist
                return JsonResponse({'error': 'plan_id not found'}, status=422)

            return JsonResponse({'plan': list(plan)})


@csrf_exempt
def update_plan(request, id):
    if request.method != 'PUT':  # If method is not PUT return error
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:  # If request method == PUT
        plan_data = json.loads(request.body)
        form = PlanForm(plan_data)
        if form.is_valid():  # Validate data
            plan = Plan.objects.get(pk=id)
            plan.name = form.cleaned_data['name']
            plan.minimum_amount = form.cleaned_data['minimum_amount']
            plan.lower_percentage = form.cleaned_data['lower_percentage']
            plan.higher_percentage = form.cleaned_data['higher_percentage']
            plan.save()

            body_content = {
                'id_plan': id
            }

            # Return updated_sale id
            return JsonResponse(body_content, status=200)

        # Since body not valid, return errors
        else:
            return JsonResponse(form.errors, status=422)


@csrf_exempt
def delete_plan(request, id):
    if request.method != 'DELETE':   # If method is not DELETE return error
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    else:  # If request method == DELETE
        try:  # Check if the plan exists
            plan = Plan.objects.get(pk=id)
        except:  # Returns an error in JSON format if sale doesn't exist
            return JsonResponse({'error': 'plan_id not found'}, status=422)
        else:  # If sale exists, delete.
            plan.delete()

            response_body = {
                'id_plan_deleted': id
            }

            return JsonResponse(response_body, status=200)
