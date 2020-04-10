## Standard Unix Development Tools ##

`bison`

A yacc-compatible parser generator.

`cvs`

A high-level revision control system that sits on top of RCS.

`flex`, `flex++`

A tool that generates lexical analyzers. See lex & yacc (O'Reilly).

`cc`, `gcc`

Apple's customized version of gcc, the GNU C compiler.

`gdb`

A source-level debugger.

`gnumake`, `make`

Tools that automate the steps necessary to compile a source code package.

`rcs`

A command that manages file revisions.

`unzip`

A tool that extracts files from a zip archive.

`zip`

A command that creates a zip archive.

-----------------------------


## Apple's Command-line Developer Tools ##

`agvtool`

Acts as a versioning tool for Project Builder projects.

`BuildStrings`

Creates resource string definitions.

`CpMac`

Serves as an alternative to cp; preserves resource forks when copying.

`cvs-unwrap`

Extracts a tar file created by cvs-wrap.

`cvs-wrap`

Combines a directory into a single tar file.

`cvswrappers`

Checks an entire directory into CVS as a binary file.

`DeRez`

Displays the contents of a resource fork.

`GetFileInfo`

Displays extended information about a file, including creator code and file type.

`lnresolve`

Returns the target of a symbolic link.

`MergePef`

Merges code fragments from one file into another.

`MvMac`

Serves as an alternative to mv; preserves resource forks when copying.

`pbhelpindexer`

Creates an index of Apple's API documentation for Project Builder.

`pbprojectdump`

Used by Project Builder's FileMerge feature to produce more readable diffs between file versions.

`pbxcp`

Supports Project Builder's build system; an internal tool.

`pbxhmapdump`

Debugs header maps; also internal to Project Builder.

`ResMerger`

Merges resource manager resource files. Project Builder's build system compiles .r files into .rsrc files using Rez, and if needed, Project Builder merges multiple files using ResMerger.

`Rez`

Compiles resource files.

`RezWack`

Embeds resource and data forks in a file.

`sdp`

Converts a scripting definition file into another format.

`SetFile`

Sets HFS+ file attributes.

`SplitForks`

Splits the resource fork, moving it from a dual-forked file into a file named ._pathname.

`UnRezWack`

Removes resource and data forks from a file.

`WSMakeStubs`

Generates web service stubs from a WSDL file.

-----------------------------


## Macintosh Tools ##

`bless`

Makes a system folder bootable.

`diskutil`

Manipulates disks and volumes.

`ditto`

Copies directories, and optionally includes resource forks for copied files.

`hdiutil`

Manipulates disk images.

`installer`

Installs packages; command-line tool.

`lsbom`

Lists the contents of a Bill of Materials (bom) file, such as the .bom files deposited under /Library/Receipts.

`open`

Opens a file or directory.

`pbcopy`

Copies standard input to the clipboard.

`pbpaste`

Sends the contents of the clipboard to standard output.

`screencapture`

Takes a screenshot of a window or the screen.

`serversetup`

Configures network adapter properties.

-----------------------------


## Java Development Tools ##

`appletviewer`

A Java applet viewer.

`jar`

A Java archive tool.

`java`

The Java Virtual Machine.

`javac`

The Java compiler.

`javadoc`

A Java documentation generator.

`javah`

A tool that generates C and header files for JNI programming.

`javap`

A tool that disassembles class files and inspects member signatures.

`jdb`

The Java Debugger.

`jikes`

A fast open source Java compiler.

-----------------------------


## Text Editing and Processing ##

`awk`

A pattern-matching language for textual database files.

`cut`

A tool that selects columns for display.

`emacs`

GNU Emacs.

`ex`

A line editor underlying vi.

`fmt`

A tool that produces roughly uniform line length.

`groff`

A document formatting system that can render troff typesetting macros to PostScript, HTML, and other formats.

`join`

A tool that merges different columns into a database.

`paste`

A utility that merges columns or switches their order.

`pico`

A simple text editor designed for use with the Pine mailer. Note that the version of pine that ships with Mac OS X is much older than the current release.

`sed`

A stream editor.

`texi2html`

A tool that converts Texinfo to HTML.

`tr`

A command that substitutes or deletes characters.

`vi`

A visual text editor.

-----------------------------


## Scripting and Shell Programming ##

`echo`

A command that repeats command-line arguments on standard output.

`expr`

A command that performs arithmetic and comparisons.

`line`

A command that reads a line of input.

`lockfile`

A command that makes sure that a file is accessed by only one script at a time.

`perl`

The Practical Extraction and Report Language.

`printf`

A command that formats and prints command-line arguments.

`sh`

A standard Unix shell.

`sleep`

A command that causes a pause during processing.

`tclsh`

The Tool Command Language (Tcl) shell.

`test`

A command that tests a condition.

`xargs`

A command that reads arguments from standard input and passes them to a command.

`zsh`

An enhanced Unix shell.


-----------------------------


## Working with Files and Directories ##

`cat`

Concatenates and displays files.

`cd`

Changes directory.

`chflags`

Changes file flags.

`chmod`

Changes access modes on files.

`cmp`

Compares two files, byte by byte.

`comm`

Compares two sorted files.

`cp`

Copies files.

`diff`

Compares two files, line by line.

`diff3`

Compares three files.

`file`

Determines a file's type.

`head`

Shows the first few lines of a file.

`less`

Serves as an enhanced alternative to more.

`ln`

Creates symbolic or hard links.

`ls`

Lists files or directories.

`mkdir`

Makes a new directory.

`more`

Displays files one screen at a time.

`mv`

Moves or renames files or directories.

`patch`

Merges a set of changes into a file.

`pwd`

Prints the working directory.

`rcp`

Insecurely copies a file to or from a remote machine. Use scp instead.

`rm`

Removes files.

`rmdir`

Removes directories.

`scp`

Secures alternative to rcp.

`sdiff`

Compares two files, side-by-side and line-by-line.

`split`

Splits files evenly.

`tail`

Shows the last few lines of a file.

`vis`

Displays nonprinting characters in a readable form.

`unvis`

Restores the output of vis to its original form.

`wc`

Counts lines, words, and characters.

`zcmp`

Compares two compressed files, byte-by-byte.

`zdiff`

Compare two compressed files, line-by-line.

-----------------------------


## File Compression and Storage ##

`compress`

A tool that compresses files to free up space (use gzip instead).

`cpio`

A utility that copies archives in or out.

`gnutar`

The GNU version of tar; available only if you have installed the Developer Tools package.

`gunzip`

A tool that uncompresses a file that was compressed with gzip.

`gzcat`

A utility that displays contents of compressed files.

`gzip`

A tool that compresses a file with Lempel-Ziv encoding.

`tar`

A tape archive tool. GNU tar has more features and fewer limitations.

`uncompress`

A utility that expands compressed (.Z) files.

`zcat`

A tool that displays contents of compressed files.

-----------------------------


## Searching and Sorting ##

`egrep`

An extended version of grep.

`fgrep`

A tool that searches files for literal words.

`find`

A utility that searches the system for filenames.

`grep`

A tool that searches files for text patterns.

`locate`

A faster version of find; however, it depends on a database that is periodically updated by the weekly cron job in /etc/weekly. If the database is out of date, find will be more accurate.

`sort`

A tool that sorts a file (use -n for numeric sorting, -u to eliminate duplicates).

`strings`

A tool that searches binary files for text patterns.

`uniq`

A utility that reports or filters duplicate lines in a file.

`zgrep`

A tool that searches compressed files for text patterns.

-----------------------------


## Miscellaneous Tools ##

`apropos`

Locates commands by keyword.

`clear`

Clears the screen.

`dc`

Serves as a reverse-polish arbitrary precision calculator.

`man`

Gets information on a command.

`nice`

Changes a job's priority.

`nohup`

Keeps a job running even if you log out.

`passwd`

Changes your password.

`script`

Produces a transcript of your login session.

`su`

Allows you to become the superuser.

`sudo`

Executes a command as another user.
