import graphene
from graphene_django import DjangoObjectType
from intent_capture.models import IntentCapture, ProgramSpec
from parametric_generator.models import GeneratedModel, AssetType
from compliance_engine.models import ComplianceCheck, RulePack
from analytics.models import AnalyticsRun

class IntentCaptureType(DjangoObjectType):
    class Meta:
        model = IntentCapture
        fields = '__all__'

class ProgramSpecType(DjangoObjectType):
    class Meta:
        model = ProgramSpec
        fields = '__all__'

class AssetTypeType(DjangoObjectType):
    class Meta:
        model = AssetType
        fields = '__all__'

class GeneratedModelType(DjangoObjectType):
    class Meta:
        model = GeneratedModel
        fields = '__all__'

class ComplianceCheckType(DjangoObjectType):
    class Meta:
        model = ComplianceCheck
        fields = '__all__'

class RulePackType(DjangoObjectType):
    class Meta:
        model = RulePack
        fields = '__all__'

class AnalyticsRunType(DjangoObjectType):
    class Meta:
        model = AnalyticsRun
        fields = '__all__'

class Query(graphene.ObjectType):
    all_intents = graphene.List(IntentCaptureType)
    intent_by_id = graphene.Field(IntentCaptureType, id=graphene.Int())
    all_specs = graphene.List(ProgramSpecType)
    all_generated_models = graphene.List(GeneratedModelType)
    all_compliance_checks = graphene.List(ComplianceCheckType)
    all_analytics_runs = graphene.List(AnalyticsRunType)

    def resolve_all_intents(root, info):
        return IntentCapture.objects.all()

    def resolve_intent_by_id(root, info, id):
        return IntentCapture.objects.filter(id=id).first()

    def resolve_all_specs(root, info):
        return ProgramSpec.objects.all()

    def resolve_all_generated_models(root, info):
        return GeneratedModel.objects.all()

    def resolve_all_compliance_checks(root, info):
        return ComplianceCheck.objects.all()

    def resolve_all_analytics_runs(root, info):
        return AnalyticsRun.objects.all()

class Mutation(graphene.ObjectType):
    process_intent = graphene.Field(ProgramSpecType, intent_id=graphene.Int())

    def mutate_process_intent(root, info, intent_id):
        intent = IntentCapture.objects.get(id=intent_id)
        if intent.status == 'processed':
            raise Exception("Already processed")
        spec_data = {"floors": 3, "width": 20, "height": 10}  # LLM stub
        spec = ProgramSpec.objects.create(intent=intent, json_spec=spec_data)
        intent.status = 'processed'
        intent.save()
        return spec

schema = graphene.Schema(query=Query, mutation=Mutation)