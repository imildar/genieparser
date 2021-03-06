expected_output = {
    "sort": {
        1: {
            "invoked": 3321960,
            "usecs": 109,
            "tty": 0,
            "one_min_cpu": 0.54,
            "process": "PIM Process",
            "five_min_cpu": 0.48,
            "runtime": 362874,
            "pid": 368,
            "five_sec_cpu": 1.03,
        },
        2: {
            "invoked": 1466728,
            "usecs": 2442,
            "tty": 0,
            "one_min_cpu": 0.87,
            "process": "IOSv e1000",
            "five_min_cpu": 2.77,
            "runtime": 3582279,
            "pid": 84,
            "five_sec_cpu": 0.55,
        },
        3: {
            "invoked": 116196,
            "usecs": 976,
            "tty": 0,
            "one_min_cpu": 0.07,
            "process": "OSPF-1 Hello",
            "five_min_cpu": 0.07,
            "runtime": 113457,
            "pid": 412,
            "five_sec_cpu": 0.15,
        },
    },
    "five_sec_cpu_total": 4,
    "five_min_cpu": 9,
    "one_min_cpu": 4,
    "nonzero_cpu_processes": ["PIM Process", "IOSv e1000", "OSPF-1 Hello"],
    "five_sec_cpu_interrupts": 0,
}
