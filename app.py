from bottle import delete, get, post, put, request, template, static_file
import requests
import utils
##############################
# Serve style
@get('/app.css')
def _():
    return static_file('app.css', '.')
##############################
# Serve Script
@get('/mixhtml.js')
def _():
    return static_file('mixhtml.js', '.')
##############################
######### LOAD INDEX #########
##############################
@get('/')
def _():
    try:
        users = utils.get_users()

        return template('views/index.html', users=users)
    except Exception as ex:
        return f"Couldn't get users!\n {ex}"
    finally:
        pass

##############################
######### CREATE USER ########
##############################
@post('/api/users')
def _():
    try:
        first_name = request.forms.get("frm_first_name")
        last_name = request.forms.get("frm_last_name")
        
        user = utils.create_user(first_name, last_name)
    
        return utils.generate_user_template(user[0], '#users', 'mix-top')
    except Exception as ex:
        return f"Couldn't create user!\n {ex}"
    finally:
        pass
##############################
### EDIT USER FIRST_NAME #####
##############################
@put('/api/users/first_name/<key>')
def _(key):
    try:
        new_first_name = request.forms.get(f"{key}_frm_first_name")

        user = utils.update_user(key, 'first_name', new_first_name)

        return utils.generate_user_template(user[0], f'#user_{str(user[0]["_key"])}', "mix-replace")
    except Exception as ex:
        return f"Couldn't edit user!\n {ex}"
    finally:
        pass
##############################
### EDIT USER LAST_NAME #####
##############################
@put('/api/users/last_name/<key>')
def _(key):
    try:
        new_last_name = request.forms.get(f"{key}_frm_last_name")

        user = utils.update_user(key, 'last_name', new_last_name)

        return utils.generate_user_template(user[0], f'#user_{str(user[0]["_key"])}', "mix-replace")
    except Exception as ex:
        return f"Couldn't edit user!\n {ex}"
    finally:
        pass
##############################
######### DELETE USER ########
##############################
@delete('/api/users/<key>')
def _(key):
    try:
        utils.delete_user(key)

        return f"""
            <template mix-target="#user_{key}" mix-replace>
                <div class="bg-red-400 flex w-48 h-36 items-center justify-center rounded-md" mix-ttl="2000">
                    User Deleted!
                </div>
            </template>
        """
    except Exception as ex:
        return f"Couldn't delete user\n {ex}"
    finally:
        pass
