"""View module for handling requests about questions"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from frssapi.models import Questions


class QuestionView(ViewSet):
    """Level up questions"""

    def retrieve(self, request, pk):
        """Handle GET requests for single question
        Returns:
            Response -- JSON serialized question instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/questions/2
            #
            # The `2` at the end of the route becomes `pk`
            question = Questions.objects.get(pk=pk)
            serializer = questionSerializer(question, context={'request': request})
            return Response(serializer.data)
        except question.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        """Handle GET requests to questions resource

        Returns:
            Response -- JSON serialized list of questions
        """
        # Get all question records from the database
        questions = Questions.objects.all()

        serializer = questionSerializer(
            questions, many=True, context={'request': request})
        return Response(serializer.data)

class questionSerializer(serializers.ModelSerializer):
    """JSON serializer for questions

    Arguments:
        serializer type
    """
    class Meta:
        model = Questions
        fields = ('id', 'text', 'explanation')
        depth = 1
