St2 CLI and Python Client
=========================

## Install from Source
Git clone the stanley repo locally, change directory to st2client, then run "python setup.py" or "python setup.py develop".

## Endpoint Configuration
By default, both the python client and the CLI will retrieve endpoint configuration from the environment. If no configuration is provided, the client will assume localhost and default ports.

* ST2_BASE_URL - Base URL for the Stanley API server endpoints (i.e. http://localhost). If only the base URL is provided, the client will assume default ports for the API servers are used. If any of the API server URL is provided, it will override the base URL and default port.
* ST2_API_URL - Endpoint for the Action REST API (i.e. http://localhost:9101) for managing actions, executions, triggers, rules and reusable configuration data.

The default endpoint configuration can be explicitly specified at the st2 CLI and the python client. For st2 CLI, the endpoints are provided via optional parameters (i.e. --url for base URL, --action-url, --reactor-url, and --datastore-url). For the python client, the endpoints are provided via the Client init as kwargs (i.e. base_url, action_url, reactor_url, and datastore_url).

## CLI
CLI is developed using standard python argparse and uses well known pattern for commands and subcommands.  In general, trigger, rule, action, and key are commands and list, get, create, update, and delete are subcommands.  The command run and execution are special cases and do not have the same set of subcommands. Please use the CLI help option for more detail description.

-h or --help option is used to display usage information.

    st2 -h
    st2 action -h
    st2 action create -h
    st2 run -h
    st2 run <action-name> -h

-j or --json option will format output as JSON.

    st2 rule get <rule-name> -j

-a or --attr option allows user to specify which attributes to display and in which order.

    st2 rule get <rule-name> -a name description

-w or --width option lets user specify the width of table columns. If only 1 value is provided, all table columns will have the same width. By default, the width is 28.

    st2 rule list -a name description -w 50
    st2 rule list -a name description -w 25 50

## Python Client

    >>> from st2client.client import Client
    >>> from st2client import models
    >>> client = Client(base_url='http://localhost')
    >>> rules = client.rules.get_all()
    >>> key_value_pair = client.keys.create(models.KeyValuePair(name='k1', value='v1'))

The models Trigger, Rule, Action, Execution, and KeyValuePair are defined under st2client.models. Please refer to the respective README section for these models for their schema.

The resource managers for the models are instantiated under the client as **triggers**, **rules**, **actions**, **executions**, and **keys**. The operations get_all, get_by_name, get_by_id, create, update, and delete are generally implemented for these resource managers.

 - **get_all** returns a list of resource instances.
 - **get_by_name** and **get_by_id** takes name and id respectively and returns the matching resource instance.
 - **create** takes a resource instance as input and creates the instance, throwing unique constraint error if name already exists
 - **update** takes a resource instance as input and updates the instance matching by name
 - **delete** takes a resource instance as input and deletes the instance matching by name