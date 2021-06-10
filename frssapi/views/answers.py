"""View module for handling requests about answers"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from frssapi.models import Answers, Questions, ScoreSheet

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

        # Create a new Python instance of the Answer class
        # and set its properties from what was sent in the
        # body of the request from the client.
        answer = Answers()
        answer.input_answer = request.data["input_answer"]
        answer.select_answer = request.data["select_answer"]
        answer.question_id = Questions.objects.get(pk=request.data["question_id"])

        # Try to save the new answer to the database, then
        # serialize the answer instance as JSON, and send the
        # JSON as a response to the client request
        try:
            answer.save()
            
            scoresheet = ScoreSheet()
            scoresheet.answer_id = answer.id
            scoresheet.user = user
            scoresheet.save()

            serializer = AnswerSerializer(answer, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

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
        # Get all answer records from the database
        answers = Answers.objects.all()

        # Support filtering answers by type
        #    http://localhost:8000/answers?type=1
        #
        # That URL will retrieve all tabletop answers
        answer_type = self.request.query_params.get('type', None)
        if answer_type is not None:
            answers = answers.filter(answertype__id=answer_type)

        serializer = AnswerSerializer(
            answers, many=True, context={'request': request})
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
    user = UserSerializer(many=False)
    class Meta:
        model = Answers
        fields = ('id', 'user', 'input_answer', 'select_answer', 'question_id')
        depth = 1
