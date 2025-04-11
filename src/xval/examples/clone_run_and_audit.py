import xval as xv

# 1. Follow instructions in README.md to setup API and authenticate. 
# 2. Set the environment name and run name below. 
# 3. Must have member or admin access to environment and a run setup therein.
# 		If you don't have an environment set up, first create one,
# 		copy a model from Xval Base, and create a run from the model. 

ENVIRONMENT_NAME = "Xval Test"
RUN_NAME = "Run"

def main(new_run_name:str|None = None):

	new_run_name = "Clone" if (new_run_name is None) else new_run_name

	# Switch to target Environment
	environment = xv.find_object("env", ENVIRONMENT_NAME)
	xv.switch_to_env(environment["uuid"])

	# Clone and initialize run
	original_run = xv.find_object("run", RUN_NAME)
	new_run = xv.clone("run", original_run["uuid"], new_run_name)
	xv.init(new_run["uuid"])
	
	# Refresh new run after initialization
	new_run = xv.retrieve("run", new_run["uuid"])

	# Optional -- Configure audit
	run_element = new_run['run_elements'][0]
	run_element['audit_config']['keep_inputs'][0]['indices'] = [0, 1]
	run_element['audit_config']['keep_vtables'][0]['values'] = [0]
	run_element['audit_config']['keep_vtables'][1]['values'] = [1]
	xv.update("run_element", run_element["uuid"], run_element)

	# Kickoff audit
	xv.audit(run_element["uuid"])


if __name__ == "__main__":
	main()


