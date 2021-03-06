from rest_framework import serializers
from .models import Review, Comment


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        
        # Validation 시 필수값에서 제외
        read_only_fields = ('review', 'user')

    def get_username(self, obj):
        return obj.user.username


# List 불러올때 사용하는 Serializer
class ReviewListSerializer(serializers.ModelSerializer):
    # comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('pk', 'title', 'movie_title', 'comment_count', 'created_at', 'user', 'username', 'rank')

    def get_username(self, obj):
        return obj.user.username


class ReviewSerializer(serializers.ModelSerializer):
    # 역참조 필드의 pk 목록에 대한 필드
    # comments = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('user',)
    
    def get_username(self, obj):
        return obj.user.username
