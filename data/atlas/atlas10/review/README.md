# Atlas-10 bounded external review

This directory contains seven case-sized claim packets, one for each Atlas-10
follow-on case. Each packet asks the five preregistered micro-questions and
binds its source and compiled-hypothesis hashes.

`review_attempts.json` is an honesty ledger, not a progress decoration. Until a
real request is sent through a real channel to an identifiable recipient, its
entry remains `not_attempted_missing_reviewer_channel`. A non-response may be
recorded after a dated attempt, but it is never relabeled as independent review.
The phase's external-attempt gate therefore remains pending at initial packet
generation.
