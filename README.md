Copyright 2009-2015 Andrew Kershaw

Licensed under the GNU Affero General Public License v3 (see
"LICENSE.txt" file).

#WARNING

This program can generate a large number of requests. Only run
sitecheck against sites you have permission to scan. Running it against
production sites is done at your own risk and not recommended without a
good understanding of the configuration options.

Do not give the authenticate module access to a CMS or site
administration area. Doing so will result in unpredictable and probably
catastrophic results.

The security module only tries to generate errors using simple attacks
and does not attempt any exploits. It will significantly increase the
number of requests however, and will also submit any forms it finds
multiple times.

#Dependencies

- Python 3
- HTML Tidy (validation, accessibility)
- Enchant, pyenchant (spelling)
- OpenSSL, pyOpenSSL, dnspython3 (domain check)

Using VirtualEnv is recommended due to the development status of some
dependencies.

#Installation

##Windows

Download and install the following:

- [Python 3](http://www.python.org/download/).

- [pyenchant](http://www.rfk.id.au/software/pyenchant/download.html) if
spellcheck is required, the Windows installer includes the Enchant
library.

- [pyopenssl](http://pypi.python.org/pypi/pyOpenSSL/) (if domain check
is required).

- [libtidy.dll](http://tidy.sourceforge.net/#binaries) if validation or
accessibility are required, place libtidy.dll on your system path, also
[see here](http://countergram.com/open-source/pytidylib/docs/index.html).

- [dnspython3](http://www.dnspython.org/) if domain check is required.

To install dnspython3 and sitecheck, extract each archive then open a
command window in the same directory as the extracted files and type:

`python setup.py install`

##Linux

Packages for dependencies should be available from your distribution's
package manager or installable via pip or the links above. Install all
dependencies and then extract the archive and run:

`python setup.py install

#Usage

##Windows

`C:\Python32\Scripts\runsitecheck.py -d http://www.domain-goes-here
C:\path\to\output`

#Linux

`runsitecheck.py -d http://www.domain-goes-here /path/to/output`

To specify the default page, use the -p switch:

`runsitecheck.py -d http://www.domain-goes-here -p home.html
/path/to/output`

See "Configuration" below for running repeated tests against the same
domain.

While running, `Ctrl+c` will prompt for abort or suspend.

To resume a suspended job or use an existing configuration file, run
the script with the path to an existing output directory:

`runsitecheck.py /path/to/output`

#Modules

- **Persister** Downloads site files to disk for further analysis,
**disabled by default**.

- **InboundLinks** Checks URLs in the search result listings from the
Google and Bing search engines, **disabled by default**.

- **RegexMatch** Checks for regular expression match in headers and
content. To search for headers which don't match a regular expression,
prefix the name with ^ and to search for content which doesn't match,
prefix with _.

- **Validator** Lists validation errors, **disabled by default**.

- **Accessibility** Outputs selected accessibility warnings that
can be automatically tested, **Disabled by default**.

- **MetaData** Checks for missing/empty/duplicate meta title, description
and keywords.

- **StatusLog** Logs any 4XX and 5XX responses. Also checks outbound links.

- **Security** Attempts basic SQL injection and XSS attacks on get and
post parameters, **disabled by default**.

- **Comments** Logs the content of any HTML comments found.

- **Spelling** Spellcheck using Enchant. Custom dictionary words are in
the file "dict.txt", **disabled by default**.

- **Spider** If this module is disabled, only a single page will be
analysed. Scans all files under the domain/path as well as testing
targets of external links.

- **Readability** Calculates the Flesch Reading Ease score and logs it if
it is below the specified threshold.

- **DuplicateContent** Checks for the same response with different URLs.

- **DomainCheck** Gets important domain information including expiry date,
SSL certificate expiry date, reverse DNS etc. Uses a whois proxy with a
limit of 50 hits per day, **disabled by default**.

- **Authenticate** Issues requests to authenticate with the target site
before spidering beings. If specified, logout requests will be executed
after spidering ends, **disabled by default**.

- **RequestList** Define a list of requests manually which are executed in
sequence, **disabled by default**.

- **RequiredPages** Creates a list of required URLs which are logged if
they are not found on the site, **disabled by default**.

- **InsecureContent** Logs insecure content referenced from secure pages.

#Configuration

Configuration for the spider and individual modules can be found in
"config.py".

For site-specific configuration, copy config.py to the output directory
specified on the command line. The domain and path properties can be
specified in the config file and subsequently omitted from the command
line (as with resuming a suspended job above). This config file will be
used instead of the default. The custom dictionary file for the
spelling module (dict.txt) can also be overridden by copying to the
same location.
