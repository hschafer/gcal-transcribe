# Google Calendar Transcription (`gcal_transcribe`)

A (hopefully small) Python project to help with moving events from one Google Calendar account to another. Note that this does not "transfer" events in the sense of moving or duplicating an event, but we use the term "transcribe" to mean that the events are recorded so that you can look back on them. The primary use case is moving from one Google account to another and wanting to preserve the history of your calendar, but you **do not** want to use an ICS export/import that will invite all your past event invitees again upon import. So while events will be made in the target calendar to mirror the original, some information will be modified and recorded differently to avoid annoying all of your friends/family/co-workers.

Running this script will require access to both the source account and the target account. It will make a copy of all events from the source calendar to the target calendar with the proper name, location, and time, but will modify the event with:

* Removing all invitees and including them as part of the event description (to avoid sending invites)
* Adding a note to the description that this event was imported from the original account.

## Installation

TODO

## Instructions

TODO