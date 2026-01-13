---
title: "RStudio Guide"
description: "RStudio Guide"
---

---

## What is R?

Similar to [Python](https://www.python.org/), [R](https://cran.r-project.org/)  is an open-source statistical software that is used to clean and analyze data. It is popular within the data science community and has many packages that make statistical modeling easier for statisticians and data scientists. To get an idea of why it might be worth learning R, [this blog post](https://www.dataquest.io/blog/three-mighty-good-reasons-to-learn-r-for-data-science/) gives a great explanation and is worth a read.

To download R, go to the [Comprehensive R Archive Network (CRAN) website](https://cran.r-project.org/) and download the version of R for your system.

You'll want to download the file similar to `R-4.2.2.pkg`. Once you've downloaded R to your machine, follow the prompts (it's best to accept the defaults) to install the software.

## What is RStudio?

RStudio is an integrated development environment (IDE) for R that is available in both open source and commercial editions. RStudio is developed by [Posit](https://posit.co/), a company that creates open source software for data science, scientific research, and technical communication. They are also responsible for many R resources and package development. Take a look at the resources page on the Posit website for more information, but below are just a couple of useful resources from RStudio.

- [Books](https://resources.rstudio.com/resources/books/)
- [Tidyverse Blog](https://www.tidyverse.org/blog/)
- [Posit Blog](https://posit.co/blog/)
- [RMarkdown Documents](https://rmarkdown.rstudio.com/)
- [A ModernDive into R and the Tidyverse](https://moderndive.netlify.app/index.html) - This book is extremely helpful to beginners explaining the difference of R and RStudio and getting familiar with how to use RStudio

**Before you download RStudio** you must first download R. *RStudio will not run if you have not downloaded R on your machine*.

**To download RStudio**, go to the Posit website and navigate through *Products > RStudio IDE > (click) Download RStudio > Download RStudio Desktop*.

Or you can just go [here](https://posit.co/download/rstudio-desktop/) and follow the steps on their website.

**NOTE** *R and RStudio may be used interchangeably throughout this page.*

## Download and Configure Snowflake Driver (MacOS)

RStudio can connect to various database for production development of models or ad hoc analysis. If you want to connect to Snowflake below are some steps to accomplish this.

1. First you will need install unixODBC using [homebrew](https://brew.sh/). If you have not already installed homebrew on your machine, the website will give you the commands to do so. Once homebrew is installed, unixODBC can be installed using the command:  `brew install unixodbc`
   - Alternatively, iODBC can be used, but this documentation uses unixODBC as the chosen driver manager.

1. This will create two configuration files, **odbcinst.ini** and **odbc.ini**.
   - **odbcinst.ini** holds the ODBC drivers information.
   - **odbc.ini** holds information required to connect to databases, such as host, username, etc. This is where you set up your DSN for your system.
   - to see the location of these configuration files, run the command `odbcinst -j`.

1. Download the latest driver for Snowflake [here](https://sfc-repo.snowflakecomputing.com/odbc/mac64/index.html). You can then follow [these instructions](https://docs.snowflake.com/developer-guide/odbc/odbc-mac) to complete the configuration of the driver on your machine.
   - As many parameters as desired can be entered in the configuration files, such as role, database, warehouse, username, etc. However, these can also be specified in RStudio. Is you choose to set up the configuration files with these details, it may be necessary to set up a DSN for every database/schema used in Snowflake.
   - Below are examples of how to configure the **odbc.ini** and **odbcinst.ini** files in the user file location.

**odbcinst.ini** (location of file based on output from the `odbcinst -j` command above)

```text
[Snowflake]
Driver      = /opt/snowflake/snowflakeodbc/lib/universal/libSnowflake.dylib
```

**odbc.ini** (location of file based on output from the `odbcinst -j` command above)

```text
[ODBC Data Sources]
SnowflakeDSII = Snowflake

[SnowflakeDSII]
Server = gitlab.snowflakecomputing.com
Port =
UID =
Schema =
Warehouse =
Driver = /opt/snowflake/snowflakeodbc/lib/universal/libSnowflake.dylib
Description = Snowflake DSII
Locale = en-US
Tracing = 0
Authenticator = gitlab.okta.com
```

[This video](https://www.youtube.com/watch?v=d0AkKsQsIZ0&list=PLy4OcwImJzBIX77cmNYiXIJ3tBhpNSUKI&index=5) shows the basic steps to connect a tool (it covers Excel) to Snowflake via ODBC.

## Connecting to Snowflake in RStudio

The next step is to connect RStudio to Snowflake using the driver configurations you've just set up. This can be accomplished by using the `DBI`,`tidyverse`, and `odbc` packages in R. For a general overview on how to connect to databases in RStudio, please refer to [this website](https://solutions.posit.co/connections/db/) for detailed information.

This is an example of the code that can be used to connect to Snowflake in R.

```json
con <- DBI::dbConnect(odbc::odbc(),
  driver = "Snowflake",
  uid = rstudioapi::askForPassword("Database UserID"),
  role = [your user role],
  warehouse = [warehouse you wish to connect to],
  pwd = rstudioapi::askForPassword("Database password"),
  Authenticator = "externalbrowser",
  database = [database you wish to connect to],
  schema = [schema you wish to connect to],
  server = "gitlab.snowflakecomputing.com"
)
```

Some details regarding the above code:

1. [**DBI**](https://dbi.r-dbi.org/) is a package that helps connect R to various databases. Above, we are using the `dbConnect()` function to pass our database parameters.
1. `odbc::odbc()` tells the function you are going to use an ODBC driver for this connection.
1. The `rstudioapi::askForPassword("")` function prompts the user to enter their UID and/or their PWD so it is not stored in their script.
1. `driver = "Snowflake"` is specific to the odbcinst.ini file set up above. This specifies which driver will be used to connect. (NOTE: if you are experiencing issues connecting, try changing the syntax to the actual path of the driver in R. Example: `driver = "/opt/snowflake/snowflakeodbc/lib/universal/libSnowflake.dylib"`.
1. `server = "gitlab.snowflakecomputing.com` is specific to the snowflake instance being accessed.

### OKTA Authenticator

Since OKTA or other authenticators are often used to connect to Snowflake, we have reference **`Authenticator`** several times in the directions above. The first is in the **odbc.ini** file, specifying the authenticator used here at GitLab (OKTA). It is then referenced in the parameters used with `DBI::dbConnect()` in the line `Authenticator = "externalbrowser"`.

The "externalbrowser" lets `dbConnect()` know it should reference the url specified in the configuration file to login to Snowflake. The password that is entered during the `rstudioapi::askForPassword()` prompt should be the users OKTA password.

Once you've completed the steps above and try running the code, you should be taken to a webpage to complete login. The console in R should display the following text before it takes you to the webpage.

`Initiating login request with your identity provider. A browser window should have opened for you to complete the login. If you can't see it, check existing browser windows, or your OS settings. Press CTRL+C to abort and try again...`

**NOTE:** You will have to stay on the webpage until it indicates your identity was confirmed and you were connected to Snowflake.

## Managing R with .Rprofile

It is recommended to set up a **.Rprofile** file to customize the startup process for a given session in RStudio. It can also simiplify sharing code with other users. Upon startup, R and RStudio will look for and run the .Rprofile file which can be used to control the behavior of your R session (e.g. setting options or environment variables).

.Rprofile files can be either at the user or project level. User-level .Rprofile files live in the base of the user's home directory, and project-level .Rprofile files live in the base of the project directory. R will source only one .Rprofile file. So if you have both a project-specific .Rprofile file and a user .Rprofile file that you want to use, you explicitly source the user-level .Rprofile at the top of your project-level .Rprofile with source("~/.Rprofile").

One easy way to edit your .Rprofile file is to use the `usethis::edit_r_profile()` function from within an R session. You can specify whether you want to edit the user or project level .Rprofile.

Follow the example below to set up a new .Rprofile file that automatically sets your username, role, and driver for snowflake. If other users follow the same template, they will not have to update this information when they access Snowflake (or any other database) tables using your code in R:

- Start by creating a blank .Rprofile document by installing packages and running the `edit_r_profile()` function from the `usethis` package

```r
install.packages("usethis")
library(usethis)
usethis::edit_r_profile()
```

- In the .Rprofile file that opens in a separate tab enter in the necessary information:

```r
.First <- function() cat("Welcome to R!")
.Last <- function()  cat("Goodbye!")

uid = "CSMITH@GITLAB.COM"
role = "CSMITH"
driver = "/opt/snowflake/snowflakeodbc/lib/universal/libSnowflake.dylib"
styler::tidyverse_style()

message("*** Successfully loaded .Rprofile ***")
```

- Save the .Rprofile file. To test if it worked, at the top of the screen in R, navigate to **Session** >> **Restart R**
- Once R has restarted the message should show up in the console. In the example above this will be `*** Successfully loaded .Rprofile ***
Welcome to R!`
- You will also see the variables `uid`, `role`, and `driver` in your environment. These variables are used for connecting to your database (Snowflake here at GitLab), or for any other variables you deem necesary.

## dbplyr

The [**dbplyr**](https://dbplyr.tidyverse.org/) package can be used to interact with databases using the tidyverse language. If you're familiar with [tidyverse](https://dbplyr.tidyverse.org/) already, you may find this package especially helpful.

## How to Use Git with RStudio

This documentation was creating using RStudio version 2022.07.1.

### Objectives

1. Set up and install Git
2. Set up Git in RStudio
3. Clone an existing project from GitLab
4. Troubleshooting

### Part 1: Installation and Setup

- Download and install [R](https://cloud.r-project.org/) (if not already installed).
- Download and install [RStudio Desktop](https://posit.co/products/open-source/rstudio/) (if not already installed).
- Install [Homebrew](https://brew.sh/) (if not already installed).
- Install Git
  - Once Homebrew is installed, open your terminal (Command+Space Bar on Mac to open search bar, and search "Terminal")
  - Run the command `brew install git` in your terminal
  - Alternatively, Git can be downloaded [HERE](https://git-scm.com/downloads). Make note of the path you install it to if you use this method.
- You will also need to have your GitLab account set up and access to the project you want to clone

### Part 2: Setting Up Git in RStudio

- Open RStudio and go to **Tools** > **Global Options** > **Git/SVN**
- Check the box labeled **Enable version control interface for RStudio project**
- Set the path to the Git executable that you just installed.
  - If you don't know where Git is installed, access your Terminal and enter command `which git` and hit the **return** key
  - The path should be something similar to `/usr/bin/git`. (Note: if navigating through Finder, hidden files can be viewed by pressing `Command` + `Shift` + `.`)
- Create an SSH key by following the instructions it/data-team/ the [Generate an SSH Key Pair](https://docs.gitlab.com/ee/user/ssh.html) section.
  - ED25519 is recommended
  - Once complete, add the private key path to the **SSH RSA Key** field
  - ![Git-SVN](/images/enterprise-data/platform/rstudio/Git1.png)
- Configure Git by setting your **GitLab user name** and **GitLab email** in RStudio
  - To open the Git prompt go to **Tools** > **Shell** and enter the following:
    - `git config --global user.name 'yourGitHubUsername'`
    - `git config --global user.email 'name@provider.com'`
- Restart RStudio

### Part 3: Create an RStudio Project with Git

- To create a new project based on a remote Git repository:
  - Select **File** > **New Project** > **Version Control**
  - ![Git-Project](/images/enterprise-data/platform/rstudio/Git2.png)
  - Choose **Git**, then provide the repository URL:
    - ![Git-Repo](/images/enterprise-data/platform/rstudio/Git3.png)
    - Access the GitLab project you want to clone
    - Select the **Clone** drop-down button at the top right
    - Copy the URL for **Clone with HTTPS**
    - ![Git-Clone](/images/enterprise-data/platform/rstudio/Git5.png)
    - Paste this link into the **Repository URL** section in RStudio
    - Select **Create New Project**
- The GitLab Project should now be visible in R Studio
- [Source](https://microsite.geo.uzh.ch/reproducible_research/post/rr-rstudio-git/) for Walkthrough Instructions

### Part 4: Troubleshooting

- Error:

  ```console
  Cloning into 'repo-name'
  gitlab.com: Permission denied (publickey).
  fatal: Could not read from remote repository.

  Please make sure you have the correct access rights and repository exists.
  ```

  - Solution: This is a known issue in certain versions of RStudio that is working to be resolved. Reinstalling an [older version](https://dailies.rstudio.com/version/2022.02.4+500.pro1/) should resolve the issue ([Source](https://forum.posit.co/t/git-authentication-error-in-rstudio/145686/2)).

## How to Update a GitLab Project with Updates from R Studio

- Before uploading changes made locally to a GitLab project ensure that you are working with the most current branch by selecting **Pull with Rebase** from the **Git** section in R (Ensure that you are rebasing from the **main** branch)
  - ![Pull](/images/enterprise-data/platform/rstudio/Pull.png)
- Once changes are complete and ready to be uploaded select the new branch icon and enter a name for the branch (no spaces allowed). Select **Create**
  - ![Push](/images/enterprise-data/platform/rstudio/Push.png)
- In the **Review Changes** window that opens in R ensure that changes on the left side of the screen are checked for **Staged** and that a commit message is entered on the right side of the screen.
- Select **Commit**
- In GitLab, navigate to the project you have made updates to. You should see a merge request that needs to be created and it will have the changes you made in R. Select the relevant reviewers and approvers to merge the changes.

## How to Connect RStudio and Google Sheets

Google Sheets and R have the ability to interact via the `googlesheets4` and `googledrive` packages in R.

1. Google App Authentication Setup
2. Package Installation
3. Reading Existing Google Sheets
4. Writing to Google Sheets

### Part 1: Google App Authentication Setup

1. Follow the steps in the [handbook](/handbook/security/corporate/systems/google/apps/) to add yourself to the Google Cloud Project.
2. Submit and issue similar to [this one](https://gitlab.com/gitlab-com/gl-security/corp/infra/issue-tracker/-/issues/877) to set up access for yourself specifically
3. Once the access is set up, you can use the below code to work through setting up and configuring access in RStudio.

```r
library(googlesheets4)
library(googledrive)
## googlesheets4 Test
google_app <- httr::oauth_app(
    "R",
    key = "[KEY].apps.googleusercontent.com",
    secret = "[SECRET]"
)

google_key <- "[GOOGLE_KEY]"

# googlesheets4::gs4_auth_configure(app = google_app,
#                                   api_key = google_key)

googlesheets4::gs4_auth_configure(client = gargle::gargle_oauth_client_from_json("~/Google Drive/Shared drives/People Analytics/Google API in R/googlesheets_api_sm.json"),
                                  api_key = google_key)

googlesheets4::gs4_auth()

## Test Read
googlesheets4::read_sheet(ss = "https://docs.google.com/spreadsheets/d/1Oe7AduRIKO7Zqh60v51Zn-WnTJYpcMDho_394urBmpA",
                          sheet = "stop_words") |>
    View()


## googledrive Test

googledrive::drive_auth()

googledrive::drive_mv(file = "[SHEET_NAME]",
         path = as_id("[PATH]"),
         overwrite = TRUE)

```

### Part 2: Installation

- Run the following code in R to install the necessary packages in RStudio

```r
pkg <- c("googlesheets4", "googledrive")
invisible(lapply(pkg, function(x) if (x %in% rownames(installed.packages())==F) install.packages(x)))
invisible(lapply(pkg, library, character.only = TRUE))
rm(pkg)
```

### Part 3: Reading Existing Google Sheets

- The `read_sheet()` function will allow you to read an existing spreadsheet
  - Run the `read_sheet()` command in R pointing to the Spreadsheet URL you want to view
  - URL example: `googlesheets4::read_sheet("https://docs.google.com/spreadsheets/...")` <br>
- When you first try to access a spreadsheet you will be prompted to enter your account information
  - Enter `Yes` in RStudio when asked "Is it Ok to cache OAuth access credentials in the folder between R Sessions"
  - You will then be prompted to log into your Google Account in the browser
  - Check the box to allow the Tidyverse API Packages to access Google Sheets spreadsheets
  - A new window will open saying authentication is complete. Close the browser window.
  - rerun the `read_sheet()` command again to confirm you can see output in R

### Part 4: Writing to Google Sheets

Below are a list of functions that can be used to write data into a Google Sheet with examples.

- **gs4_create()** can create a new spreadsheet and optionally populate initial data
  - example:

    ```r
    (ss <- gs4_create("fluffy-bunny", sheets = list(flowers = head(iris))))
    ```

- **sheet_write()** (over)writes a whole data frame into a tab within a Google Sheet.
  - example:

    ```r
    head(mtcars) %>%
    sheet_write(ss, sheet = "autos")
    ```

- **range_write()** writes/overwrites a data frame into the same range of cells in a Google Sheet. Target sheet must already exist.
  - example:

    ```r
    df <- dataframe
    ss <- "https://docs.google.com/spreadsheets/..."
    googlesheets4::range_write(ss = ss,
    data = df,
    sheet = "tabname")
    ```

- **range_clear()** can be used to clear data from an existing spreadsheet tab
  - example:

    ```r
    df <- dataframe
    ss <- "https://docs.google.com/spreadsheets/..."
    googlesheets4::range_clear(ss = ss,
    sheet = "tabname"
    range = "tabname!A2:ZZ1000000")
    ```

- **sheet_append()** can be used to add rows to an existing tab. NOTE: this function will exclude column headers as a row in the target sheet.
  - example:

    ```r
    df <- dataframe
    ss <- "https://docs.google.com/spreadsheets/..."
    googlesheets4:sheet_append(
    ss = ss,
    data = df,
    sheet = "tabname")
    ```

- [Source](https://googlesheets4.tidyverse.org/) for more information on this topic.
