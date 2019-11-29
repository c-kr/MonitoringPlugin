class MonitoringPlugin:
    def __init__(self):
        self.messages = []
        self.perfdata = []
        self.rc_human_readable = {
            0: "OK",
            1: "WARNING",
            2: "CRITICAL",
            3: "UNKNOWN" }
    
    def _get_perfdata(self):
        return " ".join(self.perfdata)
        
    def add_message(self, statuscode, message, *args):
        for arg in args:
            self.perfdata.append(arg)
            
        if 0 <= statuscode <=3:
            self.messages.append({
                "statuscode": statuscode,
                "message": message,
            })
        else:
            return
        
    def add_perfdata(self, *args):
        for arg in args:
            self.perfdata.append(arg)
        
    def check_messages(self):
        ok_messages = str()
        warning_messages = str()
        critical_messages = str()
        unknown_messages = str()
        
        if len(self.messages) == 0:
            self.add_message(3, "no message passed to check_messages")
        
        for message in self.messages:
            if message["statuscode"] == 0:
                ok_messages += message.get("message") + " - "
            elif message["statuscode"] == 1:
                warning_messages += message.get("message") + " - "
            elif message["statuscode"] == 2:
                critical_messages += message.get("message") + " - "
            elif message["statuscode"] >= 3:
                unknown_messages += message.get("message") + " - "            
        
        final_perfdata = self._get_perfdata()
        final_message = str(unknown_messages + critical_messages + warning_messages + ok_messages)[:-3]
        final_rc = max([message.get("statuscode") for message in self.messages])
        final_statuscode = self.rc_human_readable.get(final_rc,"unknown statuscode " + str(final_rc))
        return (int(final_rc), str(final_statuscode + ": " + final_message + "|" + str(final_perfdata)))
        
if __name__ == "__main__":   

    np = MonitoringPlugin()
    np.add_message(0, "ok msg", "disk=400mb")
    np.add_message(2, "crit msg", "cpuusage=100%")
    np.add_message(3, "unk msg", "free=17%")
    np.add_message(1, "warn no perfdata")

    (rc,msg)= np.check_messages()
    np.plugin_exit(rc,msg)
