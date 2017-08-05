from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="vtpl1", channel="stable")
    builder.add_common_builds()
    builder.run()
