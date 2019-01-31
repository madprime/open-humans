from rest_framework import serializers

from data_import.models import DataFile
from data_import.serializers import DataFileSerializer

from .models import (DataRequestProject,
                     DataRequestProjectMember,
                     GrantedSourcesAccess,
                     RequestSourcesAccess)


class ProjectDataSerializer(serializers.ModelSerializer):
    """
    Serialize data for a project.
    """
    request_sources_access = serializers.SerializerMethodField()

    class Meta:  # noqa: D101
        model = DataRequestProject

        authorized_members = serializers.Field()
        id_label = serializers.Field()
        type = serializers.Field()

        fields = [
            'active',
            'approved',
            'authorized_members',
            'badge_image',
            'contact_email',
            'id',
            'id_label',
            'info_url',
            'is_academic_or_nonprofit',
            'is_study',
            'leader',
            'long_description',
            'name',
            'organization',
            'request_sources_access',
            'request_username_access',
            'returned_data_description',
            'short_description',
            'slug',
            'type',
        ]

    def get_request_sources_access(self, obj):
        """
        Get the other sources this project requestes access to.
        """
        requested_sources_qs = RequestSourcesAccess.objects.filter(
            requesting_project=obj).filter(active=True)
        requested_sources = [source.requested_project.id_label
                             for source in requested_sources_qs]
        return requested_sources


class ProjectMemberDataSerializer(serializers.ModelSerializer):
    """
    Serialize data for a project member.
    """
    sources_shared = serializers.SerializerMethodField()

    class Meta:  # noqa: D101
        model = DataRequestProjectMember

        fields = [
            'created',
            'project_member_id',
            'sources_shared',
            'username',
            'data',
        ]

    username = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    def get_sources_shared(self, obj):
        """
        Get the other sources this project requestes access to.
        """
        sources_shared_qs = GrantedSourcesAccess.objects.filter(
            requesting_project=obj.project).filter(active=True)
        sources_shared = [source.requested_project.id_label
                             for source in sources_shared_qs]
        return sources_shared

    @staticmethod
    def get_username(obj):
        """
        Only return the username if the user has shared it with the project.
        """
        if obj.username_shared:
            return obj.member.user.username

        return None

    def get_data(self, obj):
        """
        Return current data files for each source the user has shared with
        the project, including the project itself.
        """
        all_files = DataFile.objects.filter(
            user=obj.member.user).exclude(
                parent_project_data_file__completed=False)
        if obj.all_sources_shared:
            files = all_files
        else:
            files = all_files.filter(
                source__in=obj.sources_shared_including_self)
        request = self.context.get('request', None)
        return [DataFileSerializer(data_file, context={'request': request}).data
                for data_file in files]

    def to_representation(self, obj):
        rep = super(ProjectMemberDataSerializer, self).to_representation(obj)

        if not rep['username']:
            rep.pop('username')

        return rep
