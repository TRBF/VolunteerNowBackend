from rest_framework import serializers
from volunteering.models import Opportunity, User, Callout, Participation, Application, Question, UserAddedParticipation, UserToCallout 

class OpportunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Opportunity 
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = User 
        fields = '__all__'

class CalloutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Callout 
        fields = '__all__'

class UserToCalloutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserToCallout 
        fields = '__all__'

class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application 
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question 
        fields = '__all__'

class UserAddedParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddedParticipation 
        fields = '__all__'
