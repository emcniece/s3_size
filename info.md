## S3 Bucket Info for Home Assistant

![release_badge](https://img.shields.io/github/v/release/hokiebrian/s3_size?style=for-the-badge)
![release_date](https://img.shields.io/github/release-date/hokiebrian/s3_size?style=for-the-badge)
[![License](https://img.shields.io/github/license/hokiebrian/s3_size?style=for-the-badge)](https://opensource.org/licenses/Apache-2.0)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge)](https://github.com/custom-components/hacs)

## Installation

This provides a sensor that shows details of a AWS S3 Bucket - size (in GB) and number of objects. You will need an `Access Key` and `Secret` from AWS that has `ListAllMyBuckets` and `List Bucket` Permissions.

### Install Custom Components

1) Make sure that [Home Assistant Community Store (HACS)](https://github.com/custom-components/hacs) is setup.
2) Go to integrations in HACS
3) Click the 3 dots in the top right corner and choose `Custom repositories`
4) Paste the following into the repository input field `https://github.com/hokiebrian/s3_size` and choose category of `Integration`
5) Click add and restart HA to let the integration load
6) Go to settings and choose `Devices & Services`
7) Click `Add Integration` and search for `S3 Bucket Info`
8) Configure the integration by copying your `Bucket Name` `AWS Credentials` when prompted

## Usage

This sensor does not update automatically due to the overhead associated with large buckets. AWS allows only 1000 objects to be fetched at a time. A Service `S3 Size Update` is provided to be used in automations, scripts, or Tap Actions. The size returned is in GB, not GiB. AWS bills using GB and the S3 console displays in GiB.   