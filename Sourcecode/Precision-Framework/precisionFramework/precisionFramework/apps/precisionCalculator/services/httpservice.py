import requests

def send_post_request(action,method):
    base_url = "http://localhost:8001"
    class_wrapper = "public class DummyClass {" + method + "}"
    #print(class_wrapper)
    payload = {'codestring': class_wrapper}
    final_url = "{base_url}/{action}".format(base_url=base_url, action=action)
    response = requests.post(final_url, data=payload)
    #print(response.text)  # TEXT/HTML
    return response



if __name__ == "__main__":
    method = """ private static String stampFilename(String filename) {
        int typeIndex = filename.lastIndexOf('.');
        if (typeIndex == -1) {
            return filename + "-" + now();
        }
        return filename.substring(0, typeIndex) + "-" + now() + filename.substring(typeIndex);
    }"""
    response = send_post_request("metrics",method)
    response_text = response.text
    parts = response_text.split("@#@")
    metadata = parts[0]
    metadata_parts = metadata.split(",")
    metric_hash = metadata_parts[7]
    print(metric_hash)
    action_tokens = parts[2]
    action_tokens_parts = action_tokens.split(",")
    for at_part in action_tokens_parts:
        token_freq_parts = at_part.split(":")
        token = token_freq_parts[0]
        freq = token_freq_parts[1]
        print(token, freq)

