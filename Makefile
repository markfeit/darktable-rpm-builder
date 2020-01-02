#
# Makefile for darktable RPM Builder
#

# Customize the following to taste:

NAME    := darktable
VERSION := 3.0.0

# Disable this to try to build locally
USE_VAGRANT := true

# Enable this to keep the VM around post-build, requiring a manual
# build of the 'clean' target to get rid of it.
KEEP_VM := false

# Disable this to skip trying to install the prerequisites
INSTALL_PREREQS := true


# NO USER-SERVICEABLE PARTS BELOW THIS LINE.


ifeq ($(USE_VAGRANT),true)
  default: build-vagrant
else
  default: build-local
endif


TARBALL=$(NAME)-$(VERSION).tar.xz
$(TARBALL):
	rm -rf "$@"
	curl --location -s -o "$@" "https://github.com/darktable-org/darktable/releases/download/release-$(VERSION)/$@"
TO_CLEAN += $(TARBALL)


SPEC=$(NAME).spec
$(SPEC): $(SPEC).raw
	sed -e 's/__VERSION__/$(VERSION)/g' $< > $@
TO_CLEAN += $(SPEC)


BUILD_DIR=rpmbuild
$(BUILD_DIR): $(TARBALL) $(SPEC)
	rm -rf $@
	mkdir -p \
		$@/BUILD \
		$@/BUILDROOT \
		$@/RPMS \
		$@/SOURCES \
		$@/SPECS \
		$@/SRPMS
	cp $(SPEC) $@/SPECS
	cp $(TARBALL) $@/SOURCES
TO_CLEAN += $(BUILD_DIR)



build-local: $(BUILD_DIR) $(SPEC) $(TARBALL)
ifeq ($(INSTALL_PREREQS),true)
#
#	Find and install the prerequisites
#
	rpmspec -P "$(SPEC)" \
	| egrep -e "^(Build)?Requires:" \
	| awk '{ print $$2 }' \
	| xargs yum -y install
endif  # INSTALL_PREREQS
#
# 	Build the RPM
#
	set -o pipefail \
		&& HOME=$(shell pwd) \
		rpmbuild -ba \
                --buildroot $(BUILD_DIR)/BUILDROOT \
                $(SPEC) 2>&1 \
	        | tee build.log
#
#	Copy out the results
#
	cp $(BUILD_DIR)/SRPMS/*.rpm .
	cp $(BUILD_DIR)/RPMS/*/*.rpm .
TO_CLEAN += build.log *.rpm



# By-products
TO_CLEAN += .ccache




#
# Vagrant Targets
#

ifeq ($(USE_VAGRANT),true)


# This can only be done after a vagrant up
SSH_CONFIG := ssh.config
$(SSH_CONFIG):
	vagrant ssh-config > $@
SCP := scp -F $(SSH_CONFIG) -q
TO_CLEAN += $(SSH_CONFIG)



VAGRANT_DIR := /vagrant
build-vagrant: $(TARBALL)
	vagrant up
	$(MAKE) $(SSH_CONFIG)
	vagrant ssh -c "sudo make -C $(VAGRANT_DIR) build-local"
	$(SCP) "default:/$(VAGRANT_DIR)/*.rpm" .
	$(SCP) "default:/$(VAGRANT_DIR)/build.log" .
ifneq ($(KEEP_VM),true)
	vagrant destroy -f
endif
TO_CLEAN += build.log *.rpm


ssh:
	vagrant ssh


clean::
	vagrant destroy -f
TO_CLEAN += .vagrant


endif  # $(USE_VAGRANT)



#
# Everything else
#

clean::
	rm -rf $(TO_CLEAN) *~
