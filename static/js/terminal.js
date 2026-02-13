async function typeCommand(elementId, command) {
    const element = document.getElementById(elementId);
    if (!element) return;
    for (let i = 0; i < command.length; i++) {
        element.textContent += command[i];
        await new Promise(resolve => setTimeout(resolve, 50 + Math.random() * 50));
    }
    await new Promise(resolve => setTimeout(resolve, 300));
}

async function runTerminal() {
    const body = document.getElementById('terminal-body');
    if (!body) return;
    
    // Set prompt hostnames
    const prompts = document.querySelectorAll('.prompt');
    prompts.forEach(p => {
        if (p.textContent.includes('archlinux')) {
            p.innerHTML = p.innerHTML.replace('archlinux', 'localhost');
        }
    });

    // Item 1
    const out1 = document.getElementById('out-1');
    if (out1) {
        out1.style.display = 'block';
        await typeCommand('cmd-1', 'whoami');
        const res1 = document.getElementById('res-1');
        if (res1) res1.style.display = 'block';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 2
    const out2 = document.getElementById('out-2');
    if (out2) {
        out2.style.display = 'block';
        await typeCommand('cmd-2', 'neofetch');
        const res2 = document.getElementById('res-2');
        if (res2) res2.style.display = 'flex';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 3
    const out3 = document.getElementById('out-3');
    if (out3) {
        out3.style.display = 'block';
        await typeCommand('cmd-3', 'ls services/');
        const res3 = document.getElementById('res-3');
        if (res3) res3.style.display = 'block';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 4
    const out4 = document.getElementById('out-4');
    if (out4) {
        out4.style.display = 'block';
        await typeCommand('cmd-4', 'ls skills/');
        const res4 = document.getElementById('res-4');
        if (res4) res4.style.display = 'flex';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 5
    const out5 = document.getElementById('out-5');
    if (out5) {
        out5.style.display = 'block';
        await typeCommand('cmd-5', 'cat projects/opentrack.md');
        const res5 = document.getElementById('res-5');
        if (res5) res5.style.display = 'block';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 10 - Non-Profit Project
    const out10 = document.getElementById('out-10');
    if (out10) {
        out10.style.display = 'block';
        await typeCommand('cmd-10', 'cat projects/non-profit-erp.md');
        const res10 = document.getElementById('res-10');
        if (res10) res10.style.display = 'block';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 6
    const out6 = document.getElementById('out-6');
    if (out6) {
        out6.style.display = 'block';
        await typeCommand('cmd-6', 'cat projects/env-craft.md');
        const res6 = document.getElementById('res-6');
        if (res6) res6.style.display = 'block';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 11 - OpenMarkdown
    const out11 = document.getElementById('out-11');
    if (out11) {
        out11.style.display = 'block';
        await typeCommand('cmd-11', 'cat projects/OpenMarkdown.md');
        const res11 = document.getElementById('res-11');
        if (res11) res11.style.display = 'block';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 12 - matrix-status
    const out12 = document.getElementById('out-12');
    if (out12) {
        out12.style.display = 'block';
        await typeCommand('cmd-12', 'cat projects/matrix-status.md');
        const res12 = document.getElementById('res-12');
        if (res12) res12.style.display = 'block';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 7 - Terminal joke
    const out7 = document.getElementById('out-7');
    if (out7) {
        out7.style.display = 'block';
        await typeCommand('cmd-7', 'uptime --status');
        const res7 = document.getElementById('res-7');
        if (res7) res7.style.display = 'block';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 8 - sudo joke
    const out8 = document.getElementById('out-8');
    if (out8) {
        out8.style.display = 'block';
        await typeCommand('cmd-8', 'sudo rm -rf / --no-preserve-root');
        const res8 = document.getElementById('res-8');
        if (res8) res8.style.display = 'block';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Item 9 - fortune
    const out9 = document.getElementById('out-9');
    if (out9) {
        out9.style.display = 'block';
        await typeCommand('cmd-9', 'fortune -s');
        const res9 = document.getElementById('res-9');
        if (res9) res9.style.display = 'block';
        body.scrollTop = body.scrollHeight;
        await new Promise(resolve => setTimeout(resolve, 500));
    }

    // Final prompt
    const finalPrompt = document.getElementById('final-prompt');
    if (finalPrompt) {
        finalPrompt.style.display = 'block';
        body.scrollTop = body.scrollHeight;
    }

    // Secondary window humor (optional, just ensuring it's seen if we added it)
    body.scrollTop = body.scrollHeight;
    
    // Show CV section
    const cvSection = document.getElementById('cv-section');
    if (cvSection) {
        cvSection.style.display = 'block';
    }
}

window.addEventListener('load', runTerminal);
