from http import HTTPStatus
import dashscope


dashscope.api_key='sk-0f9ec10e768a4f0f97ea15356525ce81'
def sample_sync_call():
    prompt_text = '用萝卜、土豆、茄子做饭，给我个菜谱。'
    resp = dashscope.Generation.call(
        # model='llama2-13b-chat-v2',
        model='qwen-max-longcontext',
        prompt=prompt_text
    )
    if resp.status_code == HTTPStatus.OK:
        print(resp.output)  # The output text
        print(resp.usage)  # The usage information
    else:
        print(resp.code)  # The error code.
        print(resp.message)  # The error message.


sample_sync_call()