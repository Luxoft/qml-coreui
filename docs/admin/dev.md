# Developing and Contributing

To develop on a listed repository from your config document you need to clone the repository in an independent development folder and build it locally. This separation helps to have always a reference build available based on the upstream source code and a developer build based on your current modified stand.

`coreui-admin` helps you here using the `dev` command. The `dev` command allows you to clone and configure a repository inside a `dev` folder. If your project has support for Qt code-review `coreui-admin` will install the code-review commit templates and add Gerrit as a remote repository. To mark a repository for code-review add a code-review property in the repository section of your config document with the name of the review path.

```yaml
neptune3-ui:
  url: git://code.qt.io/qt-apps/neptune3-ui.git
  branch: '5.13'
  build: qmake
  os: [linux, macos]
  codereview: "qt-apps/neptune3-ui"
```

You use the `dev` command like this:

```sh
coreui-admin dev neptune3-ui
```

This will create a `dev/source/neptune3-ui` and `dev/build/neptune3-ui` and after a successful build a `dev/install/neptune3-ui`. These folders are independent of your upstream tracking folders.

In this workflow, you would edit the code in the `dev/source/neptune3-ui` folder to contribute to the Neptune3 UI. You can build and if finished upstream your changes. To check the upstream you would simply update the repo using `coreui-admin update` and build your upstream version of the repo.

!!! note

    If you like to see what a command is doing, you can simply use the `--dry-run` option. The command will output a small message on how to configure Qt Creator to build and run your project.
