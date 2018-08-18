# Migrate

Will move files from one object storage location to another. Compatible with:

* AWS S3
* Rackspace Cloudfiles


### Quickstart

Install using:

`python setup.py install`

Configure your cloud provider settings in a settings file. See 
`settings.example.py` for an example.

##### Enqueue files to be moved
Enqueue a list of source and destinations from a CSV file:
`migrate --config settings.py from_csv --csv path/to/list_of_files.csv`

The CSV should hold at least a source and destination header, and the path to
the files should follow the below example:

| source | destination |
|----|----|
| s3://bucket-name/keyname.ext | cloudfiles://container-name/object.ext |

##### Move the queue of files
You can consume the queue on a local machine or a server instance. However, for
best performance you should consume the queue with a lambda function.

You can run the queue consumer using
`migrate --config settings.py consume_queue`

Or, you can deploy the queue consumer to lambda by TODO: