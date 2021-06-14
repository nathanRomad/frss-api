"""View module for handling requests about answers"""
from frssapi.views.questions import questionSerializer
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from frssapi.models import Answers, Questions, Options

class AnswerView(ViewSet):
    """Level up answers"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized answer instance
        """

        # Uses the token passed in the `Authorization` header
        # Get the user who is logged in as the userId on Answers
        user = request.auth.user
        answerList = []
        if len(request.data) == 29:
        # Create a new Python instance of the Answer class
        # and set its properties from what was sent in the
        # body of the request from the client.
            for answers in request.data:
                    answer = Answers()
                    answer.input_answer = answers["input_answer"]
                    if answers["option_id"] is not None:
                        answer.option_id = Options.objects.get(pk=answers["option_id"])
                    answer.question_id = Questions.objects.get(pk=answers["question_id"])
                    answer.user_id = user
                    # answer.save()
                    answerList.append(answer)
            user.answers_set.set(answerList, bulk=False)
            serializer = AnswerSerializer(user.answers_set, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST) 

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        # except ValidationError as ex:
        #     return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk):
        """Handle GET requests for single answer

        Returns:
            Response -- JSON serialized answer instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/answers/2
            #
            # The `2` at the end of the route becomes `pk`
            answer = Answers.objects.get(pk=pk)
            serializer = AnswerSerializer(answer, context={'request': request})
            return Response(serializer.data)
        except Answers.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk):
        """Handle PUT requests for a answer
        Returns:
            Response -- Empty body with 204 status code
        """
        answer = Answers.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Answer, get the answer record
        # from the database whose primary key is `pk`
        answer = Answers.objects.get(pk=pk)

        answer.input_answer = request.data["input_answer"]
        answer.select_answer = request.data["select_answer"]
        answer.question_id = request.data["question_id"]

        answer.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """Handle DELETE requests for a single answer

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            answer = Answers.objects.get(pk=pk)
            answer.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Answers.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to answers resource

        Returns:
            Response -- JSON serialized list of answers
        """
        user = request.auth.user
        serializer = AnswerSerializer(
            user.answers_set, many=True, context={'request': request})
        return Response(serializer.data)


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for answers
    Arguments:
        serializer type
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
        depth = 1


class AnswerSerializer(serializers.ModelSerializer):
    """JSON serializer for answers
    Arguments:
        serializer type
    """
    class Meta:
        model = Answers
        fields = ('id', 'input_answer', 'option_id', 'question_id')
        depth = 1


class ScoreSheetSerializer(serializers.ModelSerializer):
    """JSON serializer for answers
    Arguments:
        serializer type
    """
    user_id = UserSerializer(many=False)
    answer_id = AnswerSerializer(many=False)

    class Meta:
        model = User
        fields = ('user_id', 'answer_id')
        depth = 1
