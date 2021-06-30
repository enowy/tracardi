from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.domain.result import Result
from tracardi_plugin_sdk.action_runner import ActionRunner


class StartAction(ActionRunner):

    def __init__(self, *args, **kwargs):
        pass

    async def run(self, void):
        if self.debug and self.profile.id == '@debug-profile-id':
            raise ValueError("Start action can not run in debug mode without connection to Debug action.")
        return Result(port="payload", value=self.event.dict())


def register() -> Plugin:
    return Plugin(
        start=True,
        debug=False,
        spec=Spec(
            module='app.process_engine.action.v1.start_action',
            className='StartAction',
            inputs=["void"],
            outputs=["payload"],
            init=None
        ),
        metadata=MetaData(
            name='Start',
            desc='Starts workflow and copies event to payload.',
            type='flowNode',
            width=100,
            height=100,
            icon='start',
            group=["Input/Output"]
        )
    )