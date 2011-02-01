installAddons: function() {
	var stringBundle = toolbar_buttons.interfaces.StringBundleService
			.createBundle("chrome://{{chrome_name}}/locale/button.properties");
	var title = stringBundle.GetStringFromName("installaddons");
	var fp = toolbar_buttons.interfaces.FilePicker();
	fp.init(window, title, fp.modeOpen);
	fp.appendFilter(stringBundle
			.GetStringFromName("installaddons-addons"), "*.xpi; *.jar");
	fp.appendFilter(stringBundle
			.GetStringFromName("installaddons-extensions"), "*.xpi");
	fp.appendFilter(stringBundle
			.GetStringFromName("installaddons-themes"), "*.jar");
	fp.appendFilters(fp.filterAll);
	if (fp.show() == fp.returnOK) {
		var path = fp.file.path;
		var cutFileType = path.lastIndexOf(".") + 1;
		var fileType = path.substring(cutFileType);
		var fileProtocolHandler = toolbar_buttons.interfaces.IOService
									.getProtocolHandler("file")
									.QueryInterface(Ci.nsIFileProtocolHandler);
		var url = fileProtocolHandler.newFileURI(fp.file)
					.QueryInterface(Ci.nsIURL);
		if (fileType == "xpi") {
			var xpi = {};
			xpi[decodeURIComponent(url.fileBaseName)] = url.spec;
			InstallTrigger.install(xpi);
		} else if (fileType == "jar") {
			InstallTrigger.installChrome(InstallTrigger.SKIN, url.spec,
					decodeURIComponent(url.fileBaseName));
		}
	}
}

viewAddonsExceptions: function(event) {
	if(event.button == 1) {
		toolbar_buttons.openPermissions("install",
				"addons_permissions_title", "addonspermissionstext");
	}
}