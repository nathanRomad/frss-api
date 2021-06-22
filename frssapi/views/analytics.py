from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class AnalyticsView(ViewSet):

    def list(self, request):
        """Handle GET requests to answers resource
        Returns:
            Response -- JSON serialized list of answers
        """
        user = request.auth.user

        # Build out an object to send back to the front with the data calculations provided
        analysis = {
            "detailedAnalysisOne": {
                "something": something,
                "somethingElse": somethingElse
            }
        }
        # Send the object to the client
        return Response(analysis)
