from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner


class MergeProfilesAction(ActionRunner):

    def __init__(self, *args, **kwargs):
        pass

    async def run(self, void):
        self.profile.operation.merge = True
        return None


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='app.process_engine.action.v1.operations.merge_profiles_action',
            className='MergeProfilesAction',
            inputs=["void"],
            outputs=[],
            init={"onField": None},
            manual="merge_profiles_action"
        ),
        metadata=MetaData(
            name='Merge profiles',
            desc='Merges profile in storage when flow ends. This operation is expensive so use it with caution, '
                 'only where this is new PII inforamtion added.',
            type='flowNode',
            width=200,
            height=100,
            icon='merge',
            group=["Operations"]
        )
    )