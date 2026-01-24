import graphene
from graphene_django import DjangoObjectType
from apps.parametric_generator.models import Project, GeneratedIFC
from apps.compliance_engine.models import ComplianceCheck, RulePack
from apps.analytics.models import AnalyticsRun


class ProjectType(DjangoObjectType):
    class Meta:
        model = Project
        fields = "__all__"


class GeneratedIFCType(DjangoObjectType):
    class Meta:
        model = GeneratedIFC
        fields = "__all__"


class ComplianceCheckType(DjangoObjectType):
    class Meta:
        model = ComplianceCheck
        fields = "__all__"


class RulePackType(DjangoObjectType):
    class Meta:
        model = RulePack
        fields = "__all__"


class AnalyticsRunType(DjangoObjectType):
    class Meta:
        model = AnalyticsRun
        fields = "__all__"


class Query(graphene.ObjectType):
    all_projects = graphene.List(ProjectType)
    project_by_id = graphene.Field(ProjectType, id=graphene.Int())
    all_generated_ifcs = graphene.List(GeneratedIFCType)
    generated_ifc_by_id = graphene.Field(GeneratedIFCType, id=graphene.Int())
    all_compliance_checks = graphene.List(ComplianceCheckType)
    all_analytics_runs = graphene.List(AnalyticsRunType)

    def resolve_all_projects(root, info):
        return Project.objects.all()

    def resolve_project_by_id(root, info, id):
        return Project.objects.filter(id=id).first()

    def resolve_all_generated_ifcs(root, info):
        return GeneratedIFC.objects.all()

    def resolve_generated_ifc_by_id(root, info, id):
        return GeneratedIFC.objects.filter(id=id).first()

    def resolve_all_compliance_checks(root, info):
        return ComplianceCheck.objects.all()

    def resolve_all_analytics_runs(root, info):
        return AnalyticsRun.objects.all()


class Mutation(graphene.ObjectType):
    create_project = graphene.Field(
        ProjectType,
        name=graphene.String(required=True),
        project_number=graphene.String(required=True),
    )
    generate_ifc = graphene.Field(
        GeneratedIFCType,
        project_id=graphene.Int(required=True),
        asset_type=graphene.String(required=True),
    )

    def mutate_create_project(root, info, name, project_number):
        project = Project.objects.create(
            name=name,
            project_number=project_number,
            user=info.context.user,
            status="concept",
        )
        return project

    def mutate_generate_ifc(root, info, project_id, asset_type):
        project = Project.objects.get(id=project_id)
        ifc = GeneratedIFC.objects.create(
            project=project, asset_type=asset_type, status="pending"
        )
        return ifc


schema = graphene.Schema(query=Query, mutation=Mutation)
