from rest_framework import serializers
from .models import User, Post, Like

class UserSerializer(serializers.ModelSerializer):

	password = serializers.CharField(write_only=True, required=True, style={
	                                 "input_type":   "password"})

	def create(self, validated_data):
	    username = validated_data["username"]
	    email = validated_data["email"]
	    password = validated_data["password"]
	    
	    if (email and User.objects.filter(email=email).exclude(username=username).exists()):
	        raise serializers.ValidationError(
	            {"email": "Email addresses must be unique."})

	    user = User(username=username, email=email)
	    user.set_password(password)
	    user.save()
	    return user

	class Meta():
		model = User
		fields = '__all__' # i know how to select only needed fields


class PostSerializer(serializers.ModelSerializer):
	class Meta:

		model = Post
		fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
	class Meta:

		model = Like
		fields = '__all__'