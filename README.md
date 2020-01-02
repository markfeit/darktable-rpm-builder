# darktable-rpm-builder

This package uses Vagrant to build source and binary RPMs for
darktable under Fedora.

**NOTE:** This spec does not work with RHEL and derivatives, largely
beause some of the requirements can't be easily met with those 
distributions.  There are some remnants of attempts to build with
RHEL that have been left in place should someone find a way to make
them work.


## Prerequisites

 * GNU Make
 * Vagrant
 * VirtualBox


## Building the RPMs

Edit the top of `Vagrantfile`:

 * Select the box on which to build
 * Set the number of CPUs (Optional, default is a sane value)
 * Set the amount of memory (Optional, default is a sane value)

Run `make`.

At the conclusion of the process, all RPMs and SRPMs produced will be in the
current directory.


To remove anything that was produced directly or as a side effect, run
`make clean`.
