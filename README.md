# Xval SDK

Xval is the SDK and CLI tool for managing and interacting with [Xval](https://xval.io). This guide will help you get started with installation, setup, and using the various commands available.

See the [GitHub repo](https://github.com/XvalSystems/xval-sdk).

## Installation

```bash
pip install xval
```

## Setup

1. After installation, you need to configure your Xval environment. You can do this by setting your organization's slug:

```bash
xval set --slug demo  # For demo app
# OR
xval set --slug your-company-slug  # For your company's app
```

2. Next go to [Xval](https://xval.io) and create an account.

3. Finally, login with `xval login`. You'll be prompted for your email and password.

## CLI Commands

### Core Commands

#### Version
```bash
xval version
```
Shows the current version of the Xval CLI.

### User Management Commands

#### Login
```bash
xval login
```
Authenticate with your Xval account. You'll be prompted for your email and password.

#### Logout
```bash
xval logout
```
Log out from your current Xval session.

#### Status
```bash
xval status
```
Display current configuration settings including login status and environment information.

#### Set Configuration
```bash
xval set [options]
```
Set various configuration options:
- `--slug`: Set the organization slug
- `--email`: Set the user's email
- `--env`: Switch to a different Xval environment
- `--api-url`: Set a custom API URL

### Validation Commands

#### List Objects
```bash
xval list <kind> [--attr ATTRIBUTE1 ATTRIBUTE2 ...]
```
List objects of a specific kind with optional attributes to display.

#### View Objects
```bash
xval view <kind> [--name NAME] [--uuid UUID] [--attr ATTRIBUTE1 ATTRIBUTE2 ...]
```
View an object of a specific kind with optional attributes to display.

#### Create Objects
```bash
xval create <kind> [--name NAME]
```
Create a new object of the specified kind. You'll be prompted for a name if not provided.

#### Delete Objects
```bash
xval delete <kind> [--name NAME]
```
Delete an object of the specified kind. You'll be prompted for a name if not provided.

#### Clone Objects
```bash
xval clone <kind> [--name NAME] [--new-name NEW_NAME]
```
Clone an existing object. You'll be prompted for names if not provided.

#### Initialize Run
```bash
xval init [--name NAME]
```
Initialize a new run. You'll be prompted for a name if not provided.

#### Start Run
```bash
xval run [NAME]
```
Start a run. You'll be prompted for a name if not provided.

#### Audit Run
```bash
xval audit [NAME]
```
Audit a run. You'll be prompted for a name if not provided, and can select specific run elements to audit.

## Examples

1. Basic setup:
```bash
xval set --slug demo
xval login
```

2. List available data:
```bash
xval list data
```