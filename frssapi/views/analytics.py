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
        totalLiabilities = liabilities[1].input_answer - \
            liabilities[0].input_answer

        # Add Users total income with any additional income to provide a totalAssets
        assets = user.answers_set.filter(question__id__in=[4, 5])
        totalAnnualIncome = assets[1].input_answer+assets[0].input_answer

        # Users monthly income
        income = user.answers_set.filter(question__id__in=[4])
        monthlyIncome = round(income[0].input_answer/12, 2)
        retirementSavings = user.answers_set.get(question__id=25).input_answer

        # Data for bar chart
        retirementData = [
            {
                "Financial Contributions": "Actual",
                "traditional IRA": 4,
                "traditional IRAColor": "hsl(233, 70%, 50%)",
                "Roth IRA": 93,
                "Roth IRAColor": "hsl(270, 70%, 50%)",
                "Mutual Fund": 159,
                "Mutual FundColor": "hsl(319, 70%, 50%)",
                "401k": 134,
                "401kColor": "hsl(172, 70%, 50%)",
                "Stocks/Bonds": 137,
                "Stocks/BondsColor": "hsl(160, 70%, 50%)",
                "Other": 165,
                "OtherColor": "hsl(105, 70%, 50%)"
            },
            {
                "Financial Contributions": "Goal",
                "traditional IRA": 10,
                "traditional IRAColor": "hsl(204, 70%, 50%)",
                "Roth IRA": 58,
                "Roth IRAColor": "hsl(227, 70%, 50%)",
                "Mutual Fund": 114,
                "Mutual FundColor": "hsl(159, 70%, 50%)",
                "401k": 34,
                "401kColor": "hsl(320, 70%, 50%)",
                "Stocks/Bonds": 192,
                "Stocks/BondsColor": "hsl(165, 70%, 50%)",
                "Other": 37,
                "OtherColor": "hsl(255, 70%, 50%)"
            }
        ]

    #     lineData = [
    # {
    #     "id": "japan",
    #     "color": "hsl(314, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 178
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 75
    #     },
    #     {
    #         "x": "boat",
    #         "y": 82
    #     },
    #     {
    #         "x": "train",
    #         "y": 282
    #     },
    #     {
    #         "x": "subway",
    #         "y": 213
    #     },
    #     {
    #         "x": "bus",
    #         "y": 142
    #     },
    #     {
    #         "x": "car",
    #         "y": 190
    #     },
    #     {
    #         "x": "moto",
    #         "y": 183
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 22
    #     },
    #     {
    #         "x": "horse",
    #         "y": 30
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 217
    #     },
    #     {
    #         "x": "others",
    #         "y": 164
    #     }
    #     ]
    # },
    # {
    #     "id": "france",
    #     "color": "hsl(61, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 145
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 253
    #     },
    #     {
    #         "x": "boat",
    #         "y": 97
    #     },
    #     {
    #         "x": "train",
    #         "y": 88
    #     },
    #     {
    #         "x": "subway",
    #         "y": 211
    #     },
    #     {
    #         "x": "bus",
    #         "y": 212
    #     },
    #     {
    #         "x": "car",
    #         "y": 9
    #     },
    #     {
    #         "x": "moto",
    #         "y": 273
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 101
    #     },
    #     {
    #         "x": "horse",
    #         "y": 154
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 248
    #     },
    #     {
    #         "x": "others",
    #         "y": 58
    #     }
    #     ]
    # },
    # {
    #     "id": "us",
    #     "color": "hsl(282, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 25
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 143
    #     },
    #     {
    #         "x": "boat",
    #         "y": 30
    #     },
    #     {
    #         "x": "train",
    #         "y": 282
    #     },
    #     {
    #         "x": "subway",
    #         "y": 89
    #     },
    #     {
    #         "x": "bus",
    #         "y": 17
    #     },
    #     {
    #         "x": "car",
    #         "y": 0
    #     },
    #     {
    #         "x": "moto",
    #         "y": 217
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 243
    #     },
    #     {
    #         "x": "horse",
    #         "y": 123
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 131
    #     },
    #     {
    #         "x": "others",
    #         "y": 100
    #     }
    #     ]
    # },
    # {
    #     "id": "germany",
    #     "color": "hsl(278, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 287
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 176
    #     },
    #     {
    #         "x": "boat",
    #         "y": 73
    #     },
    #     {
    #         "x": "train",
    #         "y": 52
    #     },
    #     {
    #         "x": "subway",
    #         "y": 121
    #     },
    #     {
    #         "x": "bus",
    #         "y": 222
    #     },
    #     {
    #         "x": "car",
    #         "y": 237
    #     },
    #     {
    #         "x": "moto",
    #         "y": 1
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 61
    #     },
    #     {
    #         "x": "horse",
    #         "y": 269
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 15
    #     },
    #     {
    #         "x": "others",
    #         "y": 272
    #     }
    #     ]
    # },
    # {
    #     "id": "norway",
    #     "color": "hsl(50, 70%, 50%)",
    #     "data": [
    #     {
    #         "x": "plane",
    #         "y": 234
    #     },
    #     {
    #         "x": "helicopter",
    #         "y": 20
    #     },
    #     {
    #         "x": "boat",
    #         "y": 76
    #     },
    #     {
    #         "x": "train",
    #         "y": 188
    #     },
    #     {
    #         "x": "subway",
    #         "y": 86
    #     },
    #     {
    #         "x": "bus",
    #         "y": 200
    #     },
    #     {
    #         "x": "car",
    #         "y": 34
    #     },
    #     {
    #         "x": "moto",
    #         "y": 234
    #     },
    #     {
    #         "x": "bicycle",
    #         "y": 121
    #     },
    #     {
    #         "x": "horse",
    #         "y": 221
    #     },
    #     {
    #         "x": "skateboard",
    #         "y": 169
    #     },
    #     {
    #         "x": "others",
    #         "y": 41
    #     }
    #     ]
    # }
    # ]
        # Build out an object to send back to the front with the data calculations provided
        analysis = {
            "detailedAnalysisOne": {
                "totalLiabilities": totalLiabilities,
                "retirementSavings": retirementSavings
            },
            "retirementData": retirementData
        }
        # Send the object to the client
        return Response(analysis)
