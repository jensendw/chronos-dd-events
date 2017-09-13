# Chronos Datadog Event Pusher

## Overview
The chronos datadog event pusher service grabs the health status of your chronos tasks and emits the status as an event to datadog.  Your users can then setup alerts and/or subscribe to the status of their services using datadog.

## Setup

See the docker-compose.yml for what environment variables need to be set, an explanation of each variable is noted below:

* CHRONOS_URL
** The URL of the chronos servers, this is a comma delimited list of servers
* DATADOG_APP_KEY
** A datadog APP key
* DATADOG_API_KEY
** A datadog API key
* UPDATE_INTERVAL
** How often you want to check the status of your chronos tasks and emit them to datadog

## Deployment

I run this app as a marathon service with a scale of 1.

```json
{
  "id": "chronos-dd-events",
  "cpus": 0.1,
  "mem": 128.0,
  "instances": 1,
  "container": {
    "type": "DOCKER",
    "docker": {
      "image": "jensendw/chronos-dd-events:latest"
    }
  },
  "env": {
    "CHRONOS_URL": "chronos1:4400,chronos2:4400",
    "DATADOG_APP_KEY": "xxxx",
    "DATADOG_API_KEY": "yyyyy",
    "UPDATE_INTERVAL": 60
  }
}
```


## Contributing

1. Fork it ( https://github.com/jensendw/chronos-dd-events )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
