from drf_yasg import openapi


PROJECT_PARAMETERS = [
   
    openapi.Parameter(
        'search', openapi.IN_QUERY, type=openapi.TYPE_STRING,
        description="Search by name or label"),
       
    openapi.Parameter(
         'user', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
        description="pass the id of user"),
       
  
]