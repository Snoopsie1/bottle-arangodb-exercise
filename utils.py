import requests

url = 'http://arangodb:8529/_api/cursor'

def execute_query(query):
    body = { "query" : query }
    response = requests.post(url, json = body)

    if response.status_code == 201:
        data = response.json()
        result = data.get('result', [])
    else:
        raise Exception(f'Request failed with status code: {response.status_code}')

    return result
############################################################
def create_user(first_name, last_name):
    query = f"""
        INSERT {{ 'first_name': '{first_name}', 'last_name': '{last_name}' }} INTO users
        RETURN NEW
    """
    return execute_query(query)
############################################################
def get_users():
    query = f"""
            FOR user IN users 
            SORT user._key DESC
            RETURN user
        """
    return execute_query(query)
############################################################
def update_user(key, attribute, new_value):
    query = f"""
        FOR user IN users FILTER user._key == '{key}'
        UPDATE user WITH {{ {attribute}: '{new_value}' }} IN users
        RETURN NEW
    """
    return execute_query(query)
############################################################
def delete_user(key):
    query = f"""
        FOR user in users FILTER user._key == '{key}' 
        REMOVE user IN users
    """
    return execute_query(query)
############################################################
def generate_user_template(user, target, method):
            return f"""
            <template mix-target="{target}" {method}>
                <div id="user_{str(user['_key'])}" class="bg-gradient-to-r from-gray-200 to-gray-300 rounded-md flex flex-col gap-2 p-6 shadow-md">
                    <div class="flex w-full justify-between">
                       <p>ID: {str(user['_key'])}</p>
                        <button mix-delete="/api/users/{str(user['_key'])}" class="text-xl">
                           🗑️
                        </button>
                    </div>
                    <form id="edit_user_{str(user['_key'])}" class="flex flex-col gap-4">
                        <label for="{str(user['_key'])}_frm_first_name">
                             First Name:
                             <input 
                               class="border-2 border-blue-300 rounded-md p-1"
                               name="{str(user['_key'])}_frm_first_name" 
                               value="{str(user['first_name'])}"
                               type="text"
                               mix-put="/api/users/first_name/{str(user['_key'])}"
                               mix-data="#edit_user_{str(user['_key'])}"
                               mix-blur
                               >
                        </label>
                        <label for="{str(user['_key'])}_frm_last_name">
                            Last Name:
                            <input 
                            class="border-2 border-blue-300 rounded-md p-1"
                            name="{str(user['_key'])}_frm_last_name" 
                            value="{str(user['last_name'])}" 
                            type="text" 
                            mix-put="/api/users/last_name/{str(user['_key'])}"
                            mix-data="#edit_user_{str(user['_key'])}"
                            mix-blur
                            >
                       </label>
                    </form>
                </div>
            </template>
        """
############################################################