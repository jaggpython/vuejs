from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer
from rest_framework_simplejwt. authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class TodoView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        print(user)
        todos = Todo.objects.filter(user = user)
        serializer = TodoSerializer(todos, many=True)

        return Response({
            'status': True,
            'data': serializer.data,
            'message': 'todo fatched successfully'
        })

    def post(self, request):
        try:
            user = request.user
            data = request.data
            data['user'] = user.id
            serializer = TodoSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message': 'invalid fields',
                    'data': serializer.errors 
                })
            serializer.save()
            return Response({
                'status': True,
                'message': 'Todo is created',
                'data': serializer.data
            })
        except Exception as e:
            return Response({
                'status': False,
                'message': 'something went wrong',
                'data': {}
            })