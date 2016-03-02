from dkrz_forms import form_handler

import tempfile

sf = cordex_submission_form()

sf.first_name = "Stephan"
sf.last_name = "Kindermann"
sf.email = "snkinder@freenet.de"
sf.check_status = "not_checked"

form_json_file = form_to_json(sf)
fp = tempfile.TemporaryFile()
fp.write(form_json)

new_form_json = fp.read(form_json)
new_dict = json_to_dict(new_form_json)
new_dict["__type__"] = "sf"
sf_new = json.loads(new_form_json)





form_json_file.close()


