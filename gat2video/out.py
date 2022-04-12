from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://usegalaxy.eu/
    page.goto("https://usegalaxy.eu/")

    # Click text=Login or Register
    page.locator("text=Login or Register").click()
    # expect(page).to_have_url("https://usegalaxy.eu/login")

    # Click input[name="login"]
    page.locator("input[name=\"login\"]").click()

    # Fill input[name="login"]
    page.locator("input[name=\"login\"]").fill("hxr@informatik.uni-freiburg.de")

    # Click input[name="password"]
    page.locator("input[name=\"password\"]").click()

    # Fill input[name="password"]
    page.locator("input[name=\"password\"]").fill("wswTKY3Rem5knnWTakuNzrBbZ9")

    # Click button:has-text("Login")
    # with page.expect_navigation(url="https://usegalaxy.eu/"):
    with page.expect_navigation():
        page.locator("button:has-text(\"Login\")").click()

    # Click #history-new-button span
    page.locator("#history-new-button span").click()

    # Click [aria-label="Download from URL or upload files from disk"]
    page.locator("[aria-label=\"Download from URL or upload files from disk\"]").click()

    # Fill text=Name Size Type Genome Settings Status Download data from the web by entering URL >> textarea
    page.locator("text=Name Size Type Genome Settings Status Download data from the web by entering URL >> textarea").fill("https://zenodo.org/record/1156405/files/contigs.fasta\n")

    # Press Escape
    page.locator("body:has-text(\"Galaxy Europe Workflow Visualize Shared Data Data Libraries Histories Workflows \")").press("Escape")

    # Click #current-history-panel div:has-text("1 contigs.fasta") >> nth=1
    page.locator("#current-history-panel div:has-text(\"1 contigs.fasta\")").nth(1).click()

    # Click [placeholder="search tools"]
    page.locator("[placeholder=\"search tools\"]").click()

    # Fill [placeholder="search tools"]
    page.locator("[placeholder=\"search tools\"]").fill("prokka")

    # Press Enter
    page.locator("[placeholder=\"search tools\"]").press("Enter")

    # Click text=Prokaryotic genome annotation
    page.locator("text=Prokaryotic genome annotation").click()
    # expect(page).to_have_url("https://usegalaxy.eu/")

    # Click span:has-text("1: contigs.fasta")
    page.locator("span:has-text(\"1: contigs.fasta\")").click()

    # Click div[role="option"]:has-text("1: contigs.fasta")
    page.locator("div[role=\"option\"]:has-text(\"1: contigs.fasta\")").click()

    # Click button:has-text("Execute")
    page.locator("button:has-text(\"Execute\")").click()

    # Click text=Unnamed history
    page.locator("text=Unnamed history").click()

    # Fill text=13 shown178.93 KBYou are over your disk quota. Tool execution is on hold until y >> input[type="text"] >> nth=1
    page.locator("text=13 shown178.93 KBYou are over your disk quota. Tool execution is on hold until y >> input[type=\"text\"]").nth(1).fill("Playwright Prokka Test")

    # Press Enter
    page.locator("text=13 shown178.93 KBYou are over your disk quota. Tool execution is on hold until y >> input[type=\"text\"]").nth(1).press("Enter")

    # Click #dataset-4838ba20a6d867650bf94871f40d260a .primary-actions .icon-btn.display-btn .fa
    page.locator("#dataset-4838ba20a6d867650bf94871f40d260a .primary-actions .icon-btn.display-btn .fa").click()

    # Click #current-history-panel div:has-text("2 Prokka on data 1: gff") >> nth=1
    page.locator("#current-history-panel div:has-text(\"2 Prokka on data 1: gff\")").nth(1).click()

    # Click #current-history-panel div:has-text("2 Prokka on data 1: gff") >> nth=1
    page.locator("#current-history-panel div:has-text(\"2 Prokka on data 1: gff\")").nth(1).click()

    # Click text=Prokka on data 1: gff
    page.locator("text=Prokka on data 1: gff").click()

    # Click #dataset-4838ba20a6d867650bf94871f40d260a .primary-actions .icon-btn.display-btn .fa
    page.locator("#dataset-4838ba20a6d867650bf94871f40d260a .primary-actions .icon-btn.display-btn .fa").click()

    # Close page
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
