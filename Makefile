#
# Makefile for darktable RPM
#

NAME    := darktable
VERSION := 3.0.0


USE_VAGRANT := false
INSTALL_PREREQS := true

ifeq ($(USE_VAGRANT),true)
  default: build-vagrant
else
  default: build-local
endif


TARBALL=$(NAME)-$(VERSION).tar.xz
$(TARBALL):
	rm -rf "$@"
	curl --location -s -o "$@" "https://github.com/darktable-org/darktable/releases/download/release-$(VERSION)/$@"
# TODO: Enable this
#TO_CLEAN += $(TARBALL)


SPEC=$(NAME).spec


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
	cp darktable.spec $@/SPECS
	cp $(TARBALL) $@/SOURCES
TO_CLEAN += $(BUILD_DIR)



build-local: $(BUILD_DIR) $(SPEC)
ifeq ($(INSTALL_PREREQS),true)
#
#	Find and install the prerequisites
#
	rpmspec -P "$(SPEC)" \
	| egrep -e "^(Build)?Requires:" \
	| awk '{ print $$2 }' \
	| xargs echo yum -y install
endif  # INSTALL_PREREQS
#
# 	Build the RPM
#
	HOME=$(shell pwd) \
		rpmbuild -ba \
                --buildroot $(BUILD_DIR)/BUILDROOT \
                darktable.spec 2>&1 \
	        | tee build.log
#
#	Copy out the results
#
	cp $(BUILD_DIR)/SRPMS/*.rpm .
	cp $(BUILD_DIR)/RPMS/*.rpm .
TO_CLEAN += build.log *.rpm



# By-products
TO_CLEAN += .ccache




#
# Vagrant Targets
#

ifeq ($(USE_VAGRANT),true)

build-vagrant:
	vagrant up

# TODO: Need to pull the results from the VM

clean::
	vagrant destroy -f
endif  # $(USE_VAGRANT)



#
# Everything else
#

clean::
	rm -rf $(TO_CLEAN) *~
