from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class AnalyticsView(ViewSet):

    def list(self, request):
        """Handle GET requests to answers resource
        Returns:
            Response -- JSON serialized list of answers
        """
        user = request.auth.user

        # Budget & Protection
        # Subtract Users totalAssets from totalLiabilities
        liabilities = user.answers_set.filter(question__id__in=[7, 8])
        totalLiabilities = liabilities[1].input_answer - liabilities[0].input_answer

        # Add Users total income with any additional income to provide a totalAssets
        assets = user.answers_set.filter(question__id__in=[4, 5])
        totalAnnualIncome = assets[1].input_answer+assets[0].input_answer

        # Users monthly income
        income = user.answers_set.filter(question__id__in=[4])
        monthlyIncome = round(income[0].input_answer/12, 2)
        retirementSavings = user.answers_set.get(question__id=25).input_answer

        # Build out an object to send back to the front with the data calculations provided
        analysis = {
            "detailedAnalysisOne": {
                "totalLiabilities": totalLiabilities,
                "retirementSavings": retirementSavings
            }
        }
        # Send the object to the client
        return Response(analysis)
