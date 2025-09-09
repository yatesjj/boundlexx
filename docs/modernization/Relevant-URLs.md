The goal is to modernize the Boundlexx project and correct the Steam Authentication issue.
I would like to fork the Boundlexx project, modernize it according to AngellusMortis instructions and the issues pointed out.
Resolve the Steam authentication issue.
Then I will need to know how to submit the changes to https://github.com/AngellusMortis/boundlexx

Primary Goal: Meet Modernization Expections described by AngellusMortis, get the project to the desired end state.
Next Goal, fix Steam Authentication Issue
Next Goal, cleanup project

The Boundlexx Project/Repository
https://github.com/AngellusMortis/boundlexx
https://github.com/AngellusMortis/boundlexx/issues
https://github.com/AngellusMortis/boundlexx/issues/34
https://github.com/AngellusMortis/boundlexx/issues/33
https://github.com/AngellusMortis/boundlexx/issues/32
https://github.com/AngellusMortis/boundlexx/issues/31
https://github.com/AngellusMortis/boundlexx/issues/30
https://github.com/AngellusMortis/boundlexx/issues/29
https://github.com/AngellusMortis/boundlexx/issues/28
https://github.com/AngellusMortis/boundlexx/issues/27
https://github.com/AngellusMortis/boundlexx/issues/26
https://github.com/AngellusMortis/boundlexx/issues/25
https://github.com/AngellusMortis/boundlexx/issues/24
https://github.com/AngellusMortis/boundlexx/issues/23
https://github.com/AngellusMortis/boundlexx/issues/22
https://github.com/AngellusMortis/boundlexx/issues/21

https://github.com/AngellusMortis/boundlexx/pulls
https://github.com/AngellusMortis/boundlexx/pull/43
https://github.com/AngellusMortis/boundlexx/pull/42
https://github.com/AngellusMortis/boundlexx/pull/41

https://github.com/AngellusMortis/boundlexx/actions

For Issue #33Simplify/Update Project Structure
AngellusMortis
opened on Dec 25, 2024 · edited by AngellusMortis
Owner
The project structure can be simplified and modernized a bit.
Reference repo: https://github.com/AngellusMortis/ark-operator

https://forum.playboundless.com/t/boundlexx-and-boundless-api/67519/16


https://opensource.guide/
https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo
https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo
https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo


Current Forks to examine:
This is my fork: https://github.com/yatesjj/boundlexx
Other Fork to examine: https://github.com/Redlotus99/boundlexx
Reference repository for Project Struture changes as referenced in Issue #33Simplify/Update Project Structure: https://github.com/AngellusMortis/ark-operator


Optionl Boundless Icon Rendering
https://gitlab.com/willcrutchley/boundless_headless_renderer/
https://forum.playboundless.com/t/icon-renderer/55879

Possible Methods to perform Steam Authentication for Boundlexx
SteamCMD
Web session
Python
Steam Guard
Maybe others I haven't thought of

Steam Authentication Documentation
Examine to understand the Steam Authentication Process.
The goal is to ensure Steam Authentication is working for Boundlexx
https://partner.steamgames.com/doc/api
https://partner.steamgames.com/doc/api/SteamEncryptedAppTicket

https://partner.steamgames.com/doc/features/auth
https://partner.steamgames.com/doc/features/auth#client_to_client
https://partner.steamgames.com/doc/features/auth#client_to_backend_webapi
https://partner.steamgames.com/doc/features/auth#encryptedapptickets
https://partner.steamgames.com/doc/features/auth#website
https://partner.steamgames.com/doc/api/steam_api#CSteamID
https://partner.steamgames.com/doc/api/ISteamUser#GetSteamID
https://partner.steamgames.com/doc/api/ISteamGameServer
https://partner.steamgames.com/doc/features/anticheat
https://partner.steamgames.com/doc/webapi_overview
https://partner.steamgames.com/doc/api/ISteamUser#GetAuthSessionTicket
https://partner.steamgames.com/doc/api/ISteamUser#BeginAuthSession
https://partner.steamgames.com/doc/api/ISteamUser#ValidateAuthTicketResponse_t
https://partner.steamgames.com/doc/api/ISteamUser#GetAuthSessionTicket
https://partner.steamgames.com/doc/api/ISteamUser#CancelAuthTicket
https://partner.steamgames.com/doc/api/ISteamUser#EndAuthSession
https://partner.steamgames.com/doc/api/ISteamUser#ValidateAuthTicketResponse_t
https://partner.steamgames.com/doc/api/ISteamUser#BeginAuthSession
https://partner.steamgames.com/doc/api/steam_api#k_EAuthSessionResponseNoLicenseOrExpired
https://partner.steamgames.com/doc/api/ISteamUser#UserHasLicenseForApp
https://partner.steamgames.com/doc/api/ISteamUser#GetAuthTicketForWebApi
https://partner.steamgames.com/doc/api/ISteamUser#GetTicketForWebApiResponse_t
https://partner.steamgames.com/doc/webapi/ISteamUserAuth#AuthenticateUserTicket
https://steamcommunity.com/dev
https://partner.steamgames.com/doc/webapi_overview/auth#publisher-keys
https://partner.steamgames.com/doc/webapi/ISteamUser#CheckAppOwnership
https://partner.steamgames.com/doc/webapi/ISteamUser#GetPublisherAppOwnership
https://partner.steamgames.com/doc/webapi_overview/auth#publisher-keys
https://partner.steamgames.com/doc/api/ISteamUser#EncryptedAppTicketResponse_t
https://partner.steamgames.com/doc/api/ISteamUser#GetEncryptedAppTicket
https://partner.steamgames.com/doc/api/SteamEncryptedAppTicket#BDecryptTicket
https://partner.steamgames.com/doc/api/SteamEncryptedAppTicket#BIsTicketForApp
https://partner.steamgames.com/doc/api/SteamEncryptedAppTicket#GetTicketIssueTime
https://partner.steamgames.com/doc/api/SteamEncryptedAppTicket#GetTicketSteamID
https://partner.steamgames.com/doc/sdk/api/example
https://partner.steamgames.com/doc/api/SteamEncryptedAppTicket#BIsTicketForApp
https://partner.steamgames.com/doc/api/SteamEncryptedAppTicket#BUserOwnsAppInTicket
https://partner.steamgames.com/doc/store/application/dlc
http://openid.net/
http://openid.net/developers/libraries/
https://partner.steamgames.com/doc/webapi/ISteamUser#CheckAppOwnership
https://partner.steamgames.com/doc/webapi/ISteamUser#GetPublisherAppOwnership
https://partner.steamgames.com/doc/webapi_overview/auth#publisher-keys
https://partner.steamgames.com/doc/api/ISteamUser#GetAuthTicketForWebApi
https://partner.steamgames.com/doc/api/ISteamUser#GetTicketForWebApiResponse_t
https://partner.steamgames.com/doc/webapi/ISteamUserAuth#AuthenticateUserTicket
https://partner.steamgames.com/doc/features/auth#website
https://partner.steamgames.com/doc/webapi/ISteamUser#CheckAppOwnership
https://partner.steamgames.com/doc/webapi/ISteamUser#GetPublisherAppOwnership
https://partner.steamgames.com/doc/webapi_overview/auth#publisher-keys
https://partner.steamgames.com/doc/webapi/ISteamUser#CheckAppOwnership
https://partner.steamgames.com/doc/features/auth#account_linking

