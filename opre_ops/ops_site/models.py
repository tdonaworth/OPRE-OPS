from django.contrib import admin
from django.db import models


class FundingPartner(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name="Role Name")

    def __str__(self):
        return self.name


class Person(models.Model):
    DIVISIONS = [
        ("DCFD", "DCFD"),
        ("DDI", "DDI"),
        ("DEI", "DEI"),
        ("DFS", "DFS"),
        ("OD", "OD"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    roles = models.ManyToManyField(Role)
    division = models.CharField(max_length=5, choices=DIVISIONS)

    class Meta:
        verbose_name_plural = "People"

    def display_name(self):
        return self.first_name + " " + self.last_name

    display_name.short_description = "Full name"
    full_name = property(display_name)

    def __str__(self):
        return self.full_name


class CommonAccountingNumber(models.Model):
    """
    A CAN is a Common Accounting Number, which is
    used to track money coming into OPRE

    This model contains all the relevant
    descriptive information about a given CAN
    """

    ARRANGEMENT_TYPES = [
        ("OPRE Appropriation", "OPRE Appropriation"),
        ("Cost Share", "Cost Share"),
        ("IAA", "IAA"),
        ("IDDA", "IDDA"),
        ("MOU", "MOU"),
    ]

    number = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    purpose = models.TextField(default="", blank=True)
    nickname = models.CharField(max_length=30)
    arrangement_type = models.CharField(max_length=30, choices=ARRANGEMENT_TYPES)
    funding_source = models.ManyToManyField(FundingPartner)
    authorizer = models.ForeignKey(
        FundingPartner, on_delete=models.PROTECT, related_name="authorizer"
    )

    def info_for_fiscal_year(self, fy):
        return CANFiscalYear.objects.filter(can=self.id, fiscal_year=fy).first()

    def contracts_for_fiscal_year(self, fy):
        cid = [
            li.fiscal_year.line_item.contract.id
            for li in self.line_items_fy.filter(fiscal_year__fiscal_year=fy)
        ]
        return Contract.objects.filter(id__in=cid)

    class Meta:
        verbose_name_plural = "CANs"


class CANFiscalYear(models.Model):
    """
    A CAN is a Common Accounting Number, which is
    used to track money coming into OPRE

    This model contains all the relevant financial
    information by fiscal year for a given CAN
    """

    can = models.ForeignKey(CommonAccountingNumber, on_delete=models.PROTECT)
    fiscal_year = models.IntegerField()
    amount_available = models.DecimalField(max_digits=12, decimal_places=2)
    total_fiscal_year_funding = models.DecimalField(max_digits=12, decimal_places=2)
    potential_additional_funding = models.DecimalField(max_digits=12, decimal_places=2)
    can_lead = models.ManyToManyField(Person)
    notes = models.TextField(default="", blank=True)

    class Meta:
        unique_together = (
            "can",
            "fiscal_year",
        )
        verbose_name_plural = "CANs (fiscal year)"

    @property
    def additional_amount_anticipated(self):
        return self.total_fiscal_year_funding - self.amount_available


class Contract(models.Model):
    cans = models.ManyToManyField(CommonAccountingNumber, related_name="contracts")
    name = models.TextField()

    @property
    def research_areas(self):
        return [can.nickname for can in self.cans.all()]

    def contribution_by_can_for_fy(self, can, fy):
        return sum([li.funding for li in self.line_items_for_fy_and_can(fy, can)])

    def line_items_for_fy(self, fy):
        return ContractLineItemFiscalYear.objects.filter(
            line_item__contract=self.id, fiscal_year=fy
        )

    def line_items_for_fy_and_can(self, fy, can):
        return ContractLineItemFiscalYearPerCAN.objects.filter(
            fiscal_year__fiscal_year__in=[fy], can=can
        )


class ContractLineItem(models.Model):
    contract = models.ForeignKey(
        Contract, on_delete=models.CASCADE, related_name="line_items"
    )
    name = models.TextField()


class ContractLineItemFiscalYear(models.Model):
    line_item = models.ForeignKey(
        ContractLineItem, on_delete=models.CASCADE, related_name="fiscal_years"
    )
    fiscal_year = models.IntegerField()

    @property
    def contract(self):
        return self.line_item.contract

    @property
    def name(self):
        return self.line_item.name

    def for_can(self, can):
        return self.cans.filter(can=can).first()


class ContractLineItemFiscalYearPerCAN(models.Model):
    fiscal_year = models.ForeignKey(
        ContractLineItemFiscalYear, on_delete=models.CASCADE, related_name="cans"
    )
    can = models.ForeignKey(
        CommonAccountingNumber, on_delete=models.PROTECT, related_name="line_items_fy"
    )
    funding = models.DecimalField(max_digits=12, decimal_places=2)

    @property
    def contract(self):
        return self.fiscal_year.contract

    @property
    def name(self):
        return self.fiscal_year.name
