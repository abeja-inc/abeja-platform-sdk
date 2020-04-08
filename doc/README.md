# ABEJA Dataset SDK documentation

## Abstract

SDK documentation is generated by [Sphinx](http://www.sphinx-doc.org/en/master/)

## Coding Rules

- [日本語](https://github.com/abeja-inc/platform-developers-site/wiki/%E8%A1%A8%E8%A8%98%E3%83%AB%E3%83%BC%E3%83%AB)

## Deployments

### Environments 

env     | URL | Netlify
---     | --- | ---
prod    | https://sdk-spec.abeja.io/ | https://app.netlify.com/sites/sdk-spec-abeja-io
develop | https://dev-sdk-spec-abeja-io.netlify.com/ | https://app.netlify.com/sites/dev-sdk-spec-abeja-io


### Automated Deployment

This repository is automatically deployed to branch based environments.

See deployment settings below.

env     | Deploy branch | Netlify Setting 
---     | ---           | ---
prod    | `master`      | https://app.netlify.com/sites/sdk-spec-abeja-io/settings/deploys
develop | `develop`     | https://app.netlify.com/sites/dev-sdk-spec-abeja-io/settings/deploys

### Manual Deployment

This repository can be deployed by [netlify-cli](https://www.netlify.com/docs/cli/#manual-deploy).

```
$ netlify deploy -t $ACCESS_TOKEN -s $SITE_ID -p doc/build/html
```

`ACCESS_TOKEN` can be found in `~/.netlify/config` file which is generated by executing `netlify` command.
