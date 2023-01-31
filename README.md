# data-accessor-vald-web
This is a WEB API that works as a microservice within the Toposoid project.
Toposoid is a knowledge base construction platform.(see [Toposoid Root Project](https://github.com/toposoid/toposoid.git))
This microservice is a CUID wrapper for Vald (https://github.com/vdaas/vald).

[![Test And Build](https://github.com/toposoid/data-accessor-vald-web/actions/workflows/action.yml/badge.svg)](https://github.com/toposoid/data-accessor-vald-web/actions/workflows/action.yml)

## Requirements
* Docker version 20.10.x, or later
* docker-compose version 1.22.x
* The following microservices must be running
> vdaas/vald-agent-ngt:v1.6.3


## Setup
```bssh
docker-compose up -d
```

## Usage
http://localhost:9010/docs

<img width="1350" alt="" src="https://user-images.githubusercontent.com/82787843/197610813-58641c44-5690-47fc-aceb-9958891d80cf.png">

# Note
* This microservice uses 9010 as the default port.
* The vector dimension defaults to 768. If you want to change the dimension, you can change the settings in vald-config/config.yml
* This microservice uses [vdaas/vald](https://github.com/vdaas/vald)

## License
toposoid/data-accessor-vald-web is Open Source software released under the [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html).

## Author
* Makoto Kubodera([Linked Ideal LLC.](https://linked-ideal.com/))

Thank you!
