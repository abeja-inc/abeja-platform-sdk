# 2.3.5
- Update python & python packages version #104

# 2.3.4
- [OpsBeeLLM] Add methods for add-histories-dataset-apis #103
- [OpsBeeLLM] Sort get histories #102

# 2.3.3
- [OpsBeeLLM] Add search_query in get-dataset-items #101

# 2.3.2
- [OpsBeeLLM] Add search_query in get-histories #100

# 2.3.1
- [OpsBeeLLM] Enable to input_text or output_text is empty in create history

# 2.3.0
- Add OpsBeeLLM (α version) SDK (#92)
- [ABEJA Platform OpsBeeLLM] Add OpsBeeLLM SDK doc #98

# 2.2.4
- Add lifetime "1year" of datalake channel files (#89)

# 2.2.2
- fix bugs for removing typing-extentions and updating urlib.

# 2.2.1
- remove typing-extentions library in poetry dependencies.

# 2.2.0
- remove python 3.6 (#79)
- add python 3.6 dummy (#77)
- fix python version 3.9 -> 3.7 (#73, #74, #75, #76)
- fix python version in Programming Language (#71, #72)
- fix version with rc in circleci (#69, #70)
- add python 3.10, 3.11 (#68)
- fix for dependabot alerts (#67)
- Update python version 3.6 => 3.9 (#65)

# 2.1.2
- add comment about training_job_id in `APIClient.create_training_model()` (#57)
- specify less than version 4 of protobuf as a dependency to prevent tensorboardX from breaking (#58)

# 2.1.1
- remove dependencies of pkg_resources (#55)

# 2.1.0
- Work/use logger for tracking (#54)
- Handle "Stale file handle" error (#52)

# 2.0.0
- Switch python version to 3.6 (#44)

# 1.3.1
- add job_id to training.Models.create (#49)
- fix convert_to_zipfile_object (#51)
- Generating tmp filepath should not be affected by random.seed (#50)
- add sample code to create-deployment-version (#48)

# 1.3.0
- add low-level API `abeja.services.APIClient.request_service` (#47)

# 1.2.6
- add_datalake_channels_doc (#45)

# 1.2.5
- Add 20.10 images (#43)

# 1.2.4
- add typing-extensions dependency (#42)

# 1.2.3
- Support http url in dataset item datasource (#40) 
- Support nan in metrics (#41)

# 1.2.2
- add export_log option to Jobs.create (#39)

# 1.2.1
- Add abeja.training.model package (#38)

# 1.2.0
- Refactor file format (#34)
- Feature/support infinity in metric (#35)
- Support 1month Data Lake lifetime (#37)
- Deprecated abeja.models package (#36)

# 1.1.5
- Update doc about filter_archived (#31)
- support datasource basic auth (#32)
- support conflict_target in Data Lake (#33)

# 1.1.4
- Not available due to various circumstances

# 1.1.3
- Archive/Unarchive job (#30)
- Update conftest (#29)
- Make autopep8 aggressive (#28)    
- fix doc (#27)    

# 1.1.2
- add py.typed (#26)

# 1.1.1
- Relax version specifier (#25)

# 1.1.0
- Documentation for abeja.training (#23)
- Restructure training package modules (#24)
- Add abeja.training.Jobs/Job (#22)
- High Level APIs for training job definition (#20)
- Add type checker (my.py) for some files (#19)

# 1.0.10
- change create training job definition version interface (#16)
- fix precommit and apply fmt (#17)
- Send all params/metrics to statistics from tracker (#18)

# 1.0.9
- Feature/stop training job (#15)

# 1.0.8
- system-testのpipelineをtriggerするようにした。 (#14)
- Deprecate `/models` endpoint (#10) 
- remove f string (#13)
- trigger system test when sdk is released (#12)
- Remove deprecated field (#11)

# 1.0.4
- Add notebook type to notebok API (#6)
- use poetry (#7)
- Fix version specification (#8)
- Deprecate `source_code_base64` (#9)

# 1.0.3
- skipped

# 1.0.2
- register to pypi

# 1.0.0
- initial release
