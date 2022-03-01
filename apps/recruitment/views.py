from django.shortcuts import render
from rest_framework import serializers, viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


from .serializers import QuestionsSerializer, FormResponsesSerializer, SubmittedUserSerializer
from .models import Questions, FormResponses, Recruitment, SubmittedUser
# Create your views here.


# class QuestionsView(APIView):
#     queryset = Questions.objects.all()
#     serializer_class = QuestionsSerializer
#     def get(self, request, *args, **kwargs):
#         question_ = {}
#         question_tance = self.queryset.filter(question__domain="All")
#         serializer_ = self.serializer_class(question_tance, many=True)
#         question_["All"] = serializer_.data
#         if self.request.data.__contains__("Domain"):
#             for i in self.request.data["Domain"]:
#                 question_tance = self.queryset.filter(
#                     question__domain=i)
#                 serializer_ = self.serializer_class(question_tance, many=True)
#                 question_[i]=serializer_.data
#             return Response(question_, status=status.HTTP_200_OK)
#         else:
#             return Response(question_,status=status.HTTP_400_BAD_REQUEST)

class RetrieveResponseApi(APIView):
    def get(self, request):
        started = Recruitment.objects.all()[0].is_started
        if started:
            submissions = SubmittedUser.objects.all()
            response_body = []
            for submission in submissions:
                form_responses = FormResponses.objects.filter(
                    submitted_candidate_id=submission.candidate_id)
                submission_body = {}
                submission_body['id'] = submission.candidate_id
                submission_body['Name'] = submission.candidate_name
                submission_body['Mobile No.'] = submission.candidate_mobile_number
                submission_body['Email ID'] = submission.candidate_emailid
                submission_body['Domain Choices'] = submission.candidate_domain_choices
                submission_body['Year'] = submission.candidate_studying_year
                submission_body['Branch'] = submission.candidate_branch

                qna = []
                for form_response in form_responses:
                    res = {}
                    res['Question'] = form_response.question_id.question
                    res['Question_Type'] = form_response.question_id.question_type
                    res['Question_Domain'] = form_response.question_id.question_for_domain
                    res['Answer_Given'] = form_response.answer_given
                    qna.append(res)
                submission_body['QnA'] = qna
                response_body.append(submission_body)
            return Response(response_body, status=status.HTTP_200_OK)


class FormResponsesApi(APIView):
    queryset1 = SubmittedUser.objects.all()
    queryset2 = FormResponses.objects.all()

    def get(self, request):
        started = Recruitment.objects.all()[0].is_started
        if started:

            _question_ALL = Questions.objects.filter(
                question_for_domain='All').all()
            _question_WEB = Questions.objects.filter(
                question_for_domain='Web').all()
            _question_CORE = Questions.objects.filter(
                question_for_domain='Core').all()
            _question_DESIGN = Questions.objects.filter(
                question_for_domain='Design').all()
            _question_DOCS = Questions.objects.filter(
                question_for_domain='Docs').all()
            _question_PR = Questions.objects.filter(
                question_for_domain='PR').all()

            question_ALL = QuestionsSerializer(_question_ALL, many=True)
            question_WEB = QuestionsSerializer(_question_WEB, many=True)
            question_CORE = QuestionsSerializer(_question_CORE, many=True)
            question_DESIGN = QuestionsSerializer(_question_DESIGN, many=True)
            question_DOCS = QuestionsSerializer(_question_DOCS, many=True)
            question_PR = QuestionsSerializer(_question_PR, many=True)

            _question = {'ALL': question_ALL.data, 'WEB': question_WEB.data, 'CORE': question_CORE.data,
                         'DESIGN': question_DESIGN.data, 'DOCS': question_DOCS.data, 'PR': question_PR.data}
            return Response(_question, status=status.HTTP_202_ACCEPTED)

        return Response('Recruitment Not Started', status=status.HTTP_406_NOT_ACCEPTABLE)

    def post(self, request):
        started = Recruitment.objects.all()[0].is_started
        if started:
            if self.request.data.__contains__("Name") and self.request.data.__contains__("ID") and self.request.data.__contains__("Mobile") and self.request.data.__contains__("Email") and self.request.data.__contains__("Domain") and self.request.data.__contains__("Question") and self.request.data.__contains__("Branch") and self.request.data.__contains__("Year"):
                name = self.request.data["Name"]
                response_id = self.request.data["ID"]
                mobile = self.request.data["Mobile"]
                email = self.request.data["Email"]
                domain = self.request.data["Domain"]
                question = self.request.data["Question"]
                branch = self.request.data["Branch"]
                year = self.request.data["Year"]

                candidate = SubmittedUser.objects.create(
                    candidate_name=name, candidate_id=response_id, candidate_mobile_number=mobile, candidate_emailid=email, candidate_domain_choices=domain, candidate_studying_year=year, candidate_branch=branch)
                candidate.save()
                if question["All"]:
                    question_ = question["All"]
                    for q in question_:
                        question_instance = Questions.objects.filter(
                            question_id=q["ID"])
                        if question_instance.exists:
                            candiateResponse = FormResponses.objects.create(question_id=Questions.objects.get(
                                question_id=q["ID"]), submitted_candidate_id=candidate, answer_given=q["Answer"])
                            candiateResponse.save()
                if question["Web"]:
                    question_ = question["Web"]
                    for q in question_:
                        question_instance = Questions.objects.filter(
                            question_id=q["ID"])
                        if question_instance.exists:
                            candiateResponse = FormResponses.objects.create(question_id=Questions.objects.get(
                                question_id=q["ID"]), submitted_candidate_id=candidate, answer_given=q["Answer"])
                            candiateResponse.save()
                if question["PR"]:
                    question_ = question["PR"]
                    for q in question_:
                        question_instance = Questions.objects.filter(
                            question_id=q["ID"])
                        if question_instance.exists:
                            candiateResponse = FormResponses.objects.create(question_id=Questions.objects.get(
                                question_id=q["ID"]), submitted_candidate_id=candidate, answer_given=q["Answer"])
                            candiateResponse.save()
                if question["Design"]:
                    question_ = question["Design"]
                    for q in question_:
                        question_instance = Questions.objects.filter(
                            question_id=q["ID"])
                        if question_instance.exists:
                            candiateResponse = FormResponses.objects.create(question_id=Questions.objects.get(
                                question_id=q["ID"]), submitted_candidate_id=candidate, answer_given=q["Answer"])
                            candiateResponse.save()
                if question["Core"]:
                    question_ = question["Core"]
                    for q in question_:
                        question_instance = Questions.objects.filter(
                            question_id=q["ID"])
                        if question_instance.exists:
                            candiateResponse = FormResponses.objects.create(question_id=Questions.objects.get(
                                question_id=q["ID"]), submitted_candidate_id=candidate, answer_given=q["Answer"])
                            candiateResponse.save()
                if question["Docs"]:
                    question_ = question["Docs"]
                    for q in question_:
                        question_instance = Questions.objects.filter(
                            question_id=q["ID"])
                        if question_instance.exists:
                            candiateResponse = FormResponses.objects.create(question_id=Questions.objects.get(
                                question_id=q["ID"]), submitted_candidate_id=candidate, answer_given=q["Answer"])
                            candiateResponse.save()

                return Response(self.request.data["Question"]["All"][0]["ID"])
            return Response(self.request.data["Question"], status=status.HTTP_400_BAD_REQUEST)
        return Response('Recruitment Not Started', status=status.HTTP_406_NOT_ACCEPTABLE)
