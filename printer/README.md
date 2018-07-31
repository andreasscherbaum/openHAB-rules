# printer

Notify about jammed printer.


## Content

The setup for the laser printer in openHAB is documented [here](https://andreas.scherbaum.la/blog/archives/954-Install-openHAB2-bindings-using-Ansible.html), [here](https://andreas.scherbaum.la/blog/archives/955-Auto-approve-and-link-certain-inbox-items-in-openHAB-using-Ansible.html) and [here](https://andreas.scherbaum.la/blog/archives/956-Update-openHAB-Things-configuration-using-Ansible.html).

There is not much information which is provided by the printer binding, although the number of open print jobs is interesting. If this is greater than zero, it means that a job is jammed. There is a slight chance that this is measured during a print job, but so far I did not hit that problem.
